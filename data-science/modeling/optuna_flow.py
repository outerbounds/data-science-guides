from metaflow import FlowSpec, step
from metaflow.cards import Image

def objective(trial):
    from sklearn.datasets import load_iris
    from sklearn.tree import ExtraTreeClassifier
    from sklearn.model_selection import cross_val_score
    import numpy as np
    data = load_iris()
    X, y = data['data'], data['target']
    max_depth = trial.suggest_int('max_depth', 2, 16)
    criterion = trial.suggest_categorical(
        'criterion', 
        ["gini", "entropy"]
    )
    model = ExtraTreeClassifier(max_depth=max_depth, 
                                criterion=criterion)
    return np.mean(cross_val_score(model, X, y, cv=5))

class OptunaFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.optimization_loop)
        
    @step
    def optimization_loop(self):
        import optuna
        self.study = optuna.create_study() 
        self.study.optimize(objective, n_trials=10)
        self.next(self.end)
        
    @step
    def end(self):
        self.results = self.study.trials_dataframe()
    
if __name__ == "__main__":
    OptunaFlow()
