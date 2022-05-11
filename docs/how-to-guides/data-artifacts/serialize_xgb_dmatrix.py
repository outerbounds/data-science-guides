from metaflow import FlowSpec, step 
import xgboost as xgb
import numpy as np
from tempfile import NamedTemporaryFile

class SerializeXGBDataFlow(FlowSpec):
    file_name = 'xgb_data.xgb'
    
    @step
    def start(self):
        dmatrix = xgb.DMatrix(np.random.rand(5, 10))
        #highlight-start
        dmatrix.save_binary(self.file_name)
        with open(self.file_name, 'rb') as f:
            self.xgb_data = f.read()
        #highlight-end
        self.next(self.end)
    
    @step
    def end(self):
        #highlight-start
        with open(self.file_name, 'wb') as f:
            f.write(self.xgb_data)
        data = xgb.DMatrix(self.file_name)
        #highlight-end
        print(f'there are {data.num_row()} rows in the data.')
        pass
    

if __name__ == '__main__':
    SerializeXGBDataFlow()
