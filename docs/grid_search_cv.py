from metaflow import FlowSpec, step

class GridSearchCVFlow(FlowSpec):
    '''
    Do a Grid Search on an ExtraTreeClassifier using GridSearchCV. 
    
    Arguments: 
        None
    '''
    
    @step
    def start(self):
        ''' 
        Load data.
        '''
        from sklearn.datasets import load_iris
        data = load_iris()
        self.X, self.y = data['data'], data['target']
        self.next(self.grid_search_cv)
        
    @step
    def grid_search_cv(self):
        ''' 
        Do GridSearchCV and save results. 
        '''
        from sklearn.model_selection import GridSearchCV
        from sklearn.tree import ExtraTreeClassifier
        grid_estimator = GridSearchCV(
            estimator=ExtraTreeClassifier(), 
            param_grid={
              'max_depth': [2, 4, 8, 16], 
              'criterion': ['entropy', 'gini']
            }
        )
        grid_estimator.fit(X=self.X, y=self.y)
        self.results = grid_estimator.cv_results_['mean_test_score']
        self.next(self.end)
        
    @step
    def end(self):
        pass
    
if __name__ == "__main__":
    GridSearchCVFlow()
