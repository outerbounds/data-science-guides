
BASE_URL = 's3://ookla-open-data/parquet/performance/type=fixed/'
YEARS = ['2019', '2020', '2021', '2022']
S3_PATHS = [
    f'year={y}/quarter=1/{y}-01-01_performance_fixed_tiles.parquet' for y in YEARS
]

def persistent_path(y):
    return f'broadband_perf-{y}-01-01.parquet'
