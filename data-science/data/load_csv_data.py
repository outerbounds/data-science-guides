from metaflow import FlowSpec, step, IncludeFile
import pandas as pd

def save_data_locally():
    url = "https://raw.githubusercontent.com/" + \
          "Netflix/metaflow/master/metaflow"
    data_path = "/tutorials/02-statistics/movies.csv"
    local_path = "./movies.csv"
    df = pd.read_csv(url+data_path)
    df.to_csv(local_path)

class CSVFlow(FlowSpec):
    
    data = IncludeFile("data", default="./movies.csv")
    
    @step
    def start(self):
        self.next(self.use_csv)
        
    @step
    def use_csv(self):
        import pandas as pd 
        from io import StringIO
        df = pd.read_csv(StringIO(self.data),
                         index_col=0)
        f = lambda x: x < 2000
        df["is_before_2000"] = df["title_year"].apply(f)
        self.new_df = df
        self.next(self.end)
        
    @step
    def end(self):
        result = self.new_df.is_before_2000.sum() 
        print(f"Number of pre-2000 movies is {result}.")
        
if __name__ == "__main__":
    save_data_locally()
    CSVFlow()
