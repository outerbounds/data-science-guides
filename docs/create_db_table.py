import pandas as pd

def create_table(db_path, table_name, conn):
    # create dataset
    dataset = pd.DataFrame({"id": [1, 2], 
                            "feature_1": ["foo", "bar"],
                            "feature_2": ["fizz", "buzz"]})
    try: # write contents to local db
        dataset.to_sql(table_name, con=conn)
    except ValueError:
        print(f"Could not create {table_name} at {db_path}.")
