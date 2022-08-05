from metaflow import FlowSpec, step, Parameter
from sqlalchemy import create_engine
import pandas as pd

class LocalQueryFlow(FlowSpec):
    
    @step
    def start(self):        
        self.next(self.extract)
        
    @step
    def extract(self):
        QUERY = f"SELECT * FROM {table_name}"
        self.result = pd.read_sql(QUERY, con=conn)
        self.next(self.transform)
        
    @step
    def transform(self):
        f = lambda x: x["feat_1"] + x["feat_2"]
        self.result["feat_12"] = self.result.apply(f, 
                                                axis=1)
        self.next(self.write)
        
    @step
    def write(self):
        self.result.to_sql(name=f"{table_name}_updated", 
                           con=conn, 
                           if_exists="replace")
        self.next(self.end)
        
    @step
    def end(self):
        conn.close()
        
### local database configuration ###
db_path = 'mysql://root:pass@localhost/data' 
table_name = 'data' 
engine = create_engine(db_path, echo=False)
conn = engine.connect()

def create_table(db_path, table, conn):
    # create dataset
    dataset = pd.DataFrame({"id": [1, 2], 
                            "feat_1": ["foo", "bar"],
                            "feat_2": ["fizz", "buzz"]})
    try: # write contents to local db
        dataset.to_sql(table, con=conn)
    except ValueError:
        print(f"{table} at {db_path} doesn't exist.")
    
if __name__ == "__main__":
    create_table(db_path, table_name, conn)
    LocalQueryFlow()
