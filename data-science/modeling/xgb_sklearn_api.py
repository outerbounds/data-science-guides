from metaflow import FlowSpec, step, Parameter

class XGBClassifierFlow(FlowSpec):
    '''
    Fit an XGBoost model on the iris dataset using the Scikit-learn API. 
    '''

    @step
    def start(self):
        from sklearn import datasets
        self.iris = datasets.load_iris()
        self.X = self.iris['data']
        self.y = self.iris['target']
        self.next(self.train_model)
        
    @step
    def train_model(self):
        from xgboost import XGBClassifier
        from sklearn.model_selection import cross_val_score
        self.clf = XGBClassifier(eval_metric="mlogloss") 
        self.scores = cross_val_score(self.clf, self.X, self.y, cv=5)
        self.next(self.end)
        
    @step
    def end(self):
        print("Flow is done.")
    
if __name__ == "__main__":
    XGBClassifierFlow()
