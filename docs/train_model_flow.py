
from metaflow import step, FlowSpec
from model import Model

class TrainingFlow(FlowSpec, Model):
    
    @step
    def start(self):
        from sklearn import datasets
        from sklearn.model_selection import train_test_split
        self.iris = datasets.load_iris()
        X, y = self.iris['data'], self.iris['target']
        self.labels = self.iris['target_names']
        split = train_test_split(X, y, test_size=0.2)
        self.X_train, self.X_test = split[0], split[1]
        self.y_train, self.y_test = split[2], split[3]
        self.next(self.make_model)
    
    @step
    def make_model(self):
        from sklearn.ensemble import RandomForestClassifier
        self.params = {"max_depth": 8}
        self.model = self.init_model(
            model_type = RandomForestClassifier,
            params = self.params
        )
        self.next(self.train_model)
        
    @step 
    def train_model(self):
        self.model = self.train(self.model, self.X_train, self.y_train)
        self.next(self.end)
        
    @step
    def end(self):
        scores = self.score(self.model, self.X_test, self.y_test)
        print('Accuracy: ', scores['accuracy'])
    
if __name__ == "__main__":
    TrainingFlow()
