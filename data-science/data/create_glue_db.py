import pandas as pd
import awswrangler as wr

def create_db(database_name, bucket_uri, table_name):
    dataset = pd.DataFrame({
        "id": [1, 2],
        "feature_1": ["foo", "bar"],
        "feature_2": ["fizz", "buzz"]}
    )

    try: 
        # create AWS Glue database query S3 data
        wr.catalog.create_database(name=database_name)
    except wr.exceptions.AlreadyExists as error:
        # if database exists, ignore this step
        print(f"{database_name} exists!")

    # store data in AWS Data Lake
    # here we use .parquet files
        # AWS Glue works with many other data formats
    _ = wr.s3.to_parquet(df=dataset, 
                         path=f"{bucket_uri}/dataset/",
                         dataset=True, 
                         database=database_name,
                         table=table_name)
