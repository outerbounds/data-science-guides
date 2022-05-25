import pandas as pd

def save_data():
    url = "https://raw.githubusercontent.com/Netflix/metaflow/master/metaflow"
    data_path = "/tutorials/02-statistics/movies.csv"
    local_path = "./movies.csv"
    df = pd.read_csv(url+data_path)
    df.to_csv(local_path)

if __name__ == "__main__":
    save_data()
