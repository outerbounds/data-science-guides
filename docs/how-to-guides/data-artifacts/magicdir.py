from metaflow import FlowSpec, step 
#highlight-next-line
from metaflow_magicdir import magicdir
import xgboost as xgb
import numpy as np

class MagicDirFlow(FlowSpec):

    #highlight-next-line
    @magicdir(dir='mydir') # Anything you save into mydir/ will be saved as a Data Artifact
    @step
    def start(self):
        dmatrix_1 = xgb.DMatrix(np.random.rand(5, 10))
        dmatrix_2 = xgb.DMatrix(np.random.rand(13, 10))
        #highlight-start
        dmatrix_1.save_binary('mydir/dmatrix_1.xgb')
        dmatrix_2.save_binary('mydir/dmatrix_2.xgb')
        #highlight-end
        self.next(self.end)
    
    #highlight-next-line
    @magicdir(dir='mydir') # This allows you to access anything previously saved into mydir/
    @step
    def end(self):
        #highlight-start
        data_1= xgb.DMatrix('mydir/dmatrix_1.xgb')
        data_2 = xgb.DMatrix('mydir/dmatrix_2.xgb')
        #highlight-end
        print(f'data_1 has {data_1.num_row()} rows.')
        print(f'data_2 has {data_2.num_row()} rows.')

if __name__ == '__main__':
    MagicDirFlow()
