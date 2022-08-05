from metaflow import FlowSpec, step, Parameter 
import xgboost as xgb
import numpy as np
from tempfile import NamedTemporaryFile

def save_matrix(dmatrix, file_name):
    dmatrix.save_binary(file_name)
    with open(file_name, 'rb') as f:
        xgb_data = f.read()
        return xgb_data
    
def write_binary(xgb_data, file_name):
    with open(file_name, 'wb') as f:
        f.write(xgb_data)

class SerializeXGBDataFlow(FlowSpec):

    file_name = Parameter('file_name',
                          default='xgb_data.xgb')
    
    @step
    def start(self):
        dmatrix = xgb.DMatrix(np.random.rand(5, 10))
        self.xgb_data = save_matrix(dmatrix, 
                                    self.file_name) 
        self.next(self.end)
    
    @step
    def end(self):
        write_binary(self.xgb_data, self.file_name)
        data = xgb.DMatrix(self.file_name)
        print(f'there are {data.num_row()} ' + \
               'rows in the data.')
    
if __name__ == '__main__':
    SerializeXGBDataFlow()
