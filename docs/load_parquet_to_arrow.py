from metaflow import FlowSpec, step, S3

BASE_URL = 's3://ookla-open-data/' + \
           'parquet/performance/type=fixed/'
YEARS = ['2019', '2020', '2021', '2022']
S3_PATHS = [
    f'year={y}/quarter=1/{y}-' + \
     '01-01_performance_fixed_tiles.parquet' 
    for y in YEARS
]

class ParquetArrowFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.load_parquet)

    @step
    def load_parquet(self):
        import pyarrow.parquet as pq
        #highlight-start
        with S3(s3root=BASE_URL) as s3:
            tmp_data_path = s3.get_many(S3_PATHS)
            first_path = tmp_data_path[0].path
            self.table = pq.read_table(first_path)
        #highlight-end
        self.next(self.end)

    @step
    def end(self):
        print('Table for first year' + \
              f'has shape {self.table.shape}.')

if __name__ == '__main__':
    ParquetArrowFlow()
