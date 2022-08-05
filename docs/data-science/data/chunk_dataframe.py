from metaflow import FlowSpec, step

class ForEachChunkFlow(FlowSpec):
    
    bucket = "s3://outerbounds-how-tos"
    s3_path = "{}/dataframe-chunks/{}.parquet"
    df_path = "./large_dataframe.csv"
    
    @step
    def start(self):
        import pandas as pd
        from dataframe_utils import get_chunks
        my_big_df = pd.read_csv(self.df_path)
        self.table, self.chunks = get_chunks(my_big_df)
        self.next(self.process_chunk, foreach='chunks')
    
    @step
    def process_chunk(self):
        import pyarrow as pa
        import pyarrow.parquet as pq
        
        # get view of this chunk only
        chunk_id, offset, length = self.input
        chunk = self.table.slice(offset=offset, length=length)
    
        # do transformation on table
        col1 = chunk['num1'].to_numpy()
        col2 = chunk['num2'].to_numpy()
        values = pa.array(col1 * col2)
        chunk = chunk.append_column('new col', values)
    
        # write chunk as parquet file in S3 bucket
        self.my_path = self.s3_path.format(self.bucket, chunk_id)
        pq.write_table(table=chunk, where=self.my_path)
        self.next(self.join)
        
    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        import pyarrow.parquet as pq
        test_id = 'chunk_1'
        path = self.s3_path.format(self.bucket, test_id)
        test_chunk = pq.read_table(source=path)
        assert 'new col' in test_chunk.column_names
    
if __name__ == "__main__":
    ForEachChunkFlow()
