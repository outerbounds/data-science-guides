from metaflow import FlowSpec, step, Parameter
import awswrangler as wr
from create_glue_db import create_db

class AWSQueryFlow(FlowSpec):
    
    bucket_uri = Parameter(
                    "bucket_uri", 
                    default="s3://outerbounds-how-tos"
                 )
    db_name = Parameter("database_name", 
                        default="test_db")
    table_name = Parameter("table_name", 
                           default="test_table")

    @step
    def start(self):
        create_db(self.db_name, self.bucket_uri, 
                  self.table_name)
        self.next(self.query)

    @step
    def query(self):
        QUERY = f"SELECT * FROM {self.table_name}"
        result = wr.athena.read_sql_query(
            QUERY, 
            database=self.db_name
        )
        self.dataset = result
        self.next(self.transform)
        
    @step
    def transform(self):
        concat = lambda x: x["feat_1"] + x["feat_2"]
        self.dataset["feat_12"] = self.dataset.apply(
            concat, 
            axis=1
        )
        self.next(self.write)
        
    @step
    def write(self):
        path = f"{self.bucket_uri}/dataset/"
        _ = wr.s3.to_parquet(df=self.dataset, 
                             mode="overwrite",
                             path=path,
                             dataset=True, 
                             database=self.db_name,
                             table=self.table_name)
        self.next(self.end)
        
    @step
    def end(self):
        print("Database is updated!")

if __name__ == '__main__':
    AWSQueryFlow()
