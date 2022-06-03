from metaflow import FlowSpec, step, Parameter

class XGBFlow(FlowSpec):
    
    @step
    def start(self):
        from sklearn import datasets
        self.iris = datasets.load_iris()
        self.X = self.iris['data']
        self.y = self.iris['target']
        self.next(self.train_model)
    
    @step
    def train_model(self):
        import xgboost as xgb
        dtrain = xgb.DMatrix(self.X, self.y)
        self.results = xgb.cv(
            params = {'num_class':3, 
                      'objective':'multi:softmax', 
                      'eval_metric':"mlogloss"}, 
            dtrain=dtrain, 
            verbose_eval=False
        )
        self.next(self.end)
    
    @step
    def end(self):
        print("Flow is done.")

if __name__ == "__main__":
    XGBFlow()
