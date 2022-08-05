
from metaflow import step, FlowSpec
from model import Model

class ScoringFlow(FlowSpec, Model):
    
    sibling_flow = 'TrainingFlow'
    
    @step
    def start(self):
        from sklearn import datasets
        iris = datasets.load_iris()
        self.X, self.y = iris['data'], iris['target']
        self.next(self.score_trained_model)
    
    @step
    def score_trained_model(self):
        from metaflow import Flow
        run = Flow(self.sibling_flow).latest_successful_run
        self.model = run['end'].task.data.model
        self.scores = self.score(self.model, self.X, self.y)
        self.next(self.end)
        
    @step
    def end(self):
        print('Accuracy: ', self.scores['accuracy'])
    
if __name__ == "__main__":
    ScoringFlow()
