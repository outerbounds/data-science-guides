from metaflow import FlowSpec, step

class NestedForeachFlow(FlowSpec):

    @step
    def start(self):
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        iris = load_iris()
        self.X = iris['data']
        self.y = iris['target']
        self.model_param_combination = [
            (
                LogisticRegression,
                [{"C": 0.5}, {"C": 1.0}]
            ),
            (
                RandomForestClassifier, 
                [{"max_depth": 2}, {"max_depth": 6}]
            )
        ]
        #highlight-next-line
        self.next(self.tune, foreach="model_param_combination")

    @step
    def tune(self):
        self.model, self.param_dict = self.input
        #highlight-next-line
        self.next(self.train_and_score, foreach="param_dict")

    @step
    def train_and_score(self):
        from sklearn.model_selection import cross_val_score
        self.params = self.input
        self.clf = self.model(**self.params)
        self.scores = cross_val_score(
            self.clf, self.X, self.y, cv=5)
        self.next(self.join_train)

    @step
    def join_train(self, inputs):
        import json
        import numpy as np
        self.scores = {
            'model': [],
            'params': [],
            'mean accuracy': [],
            'std accuracy': [],
        }
        for i in inputs:
            self.scores['model'].append(i.clf.__class__)
            self.scores['params'].append(json.dumps(i.params))
            self.scores['mean accuracy'].append(np.mean(i.scores))
            self.scores['std accuracy'].append(np.std(i.scores))
        self.next(self.join_tune)

    @step
    def join_tune(self, inputs):
        self.all_scores = {} 
        for model in inputs:
            if self.all_scores == {}:
                self.all_scores = model.scores
            else:
                for k,v in model.scores.items():
                    self.all_scores[k] += v
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    NestedForeachFlow()
