
import pyarrow as pa
import pandas as pd
from datetime import datetime
from typing import List, Tuple

def get_chunks(df:pd.DataFrame = None,
               num_chunks:int = 4) -> Tuple[pa.Table, List]:
    get_year = lambda x: datetime.strptime(
        x.split()[0], "%Y-%m-%d").year
    df['year'] = df.date.apply(get_year)
    num_records = df.shape[0] // num_chunks
    lengths = [num_records] * num_chunks
    lengths[-1] += df.shape[0] - num_chunks*num_records
    offsets = [sum(lengths[:i]) for i in range(num_chunks)]
    names = ["chunk_%s" %i for i in range(num_chunks)]
    return (pa.Table.from_pandas(df), 
            list(zip(names, offsets, lengths)))
