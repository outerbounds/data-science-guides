from metaflow import FlowSpec, step, Flow, current, Parameter

class ModelTaggingFlow(FlowSpec):

    max_depth = Parameter('max-depth', default=2)
    tag_msg = 'Tagging run {} as a promising model'
    accuracy_threshold = 0.85

    @step
    def start(self):
        from sklearn import datasets
        from sklearn.model_selection import train_test_split
        data = datasets.load_wine()
        data = train_test_split(data['data'],
                                data['target'],
                                random_state = 42)
        self.X_train = data[0]
        self.X_test = data[1]
        self.y_train = data[2]
        self.y_test = data[3]
        self.next(self.train)

    @step
    def train(self):
        from sklearn.tree import DecisionTreeClassifier
        self.params = {
            'max_leaf_nodes': None,
            'max_depth': self.max_depth,
            'max_features' : 'sqrt',
            'random_state': 0
        }
        self.model = DecisionTreeClassifier(**self.params)
        self.model.fit(self.X_train, self.y_train)
        self.next(self.eval_and_tag)

    @step
    def eval_and_tag(self):
        from sklearn.metrics import (accuracy_score,
                                     classification_report)
        self.pred = self.model.predict(self.X_test)
        self.accuracy = float(
            accuracy_score(self.y_test, self.pred))
        print(self.accuracy)
        if self.accuracy > self.accuracy_threshold:
            print(self.tag_msg.format(current.run_id))
            run = Flow(current.flow_name)[current.run_id]
            run.add_tag('promising model')
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    ModelTaggingFlow()
