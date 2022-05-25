from metaflow import FlowSpec, step
import wandb
from wandb.integration.metaflow import wandb_log

# @wandb_log tracks each Metaflow step in a Weights and Biases run.
@wandb_log(datasets=True, models=False, others=False, 
           settings={"mode":"offline"})
class TrackedFlow(FlowSpec):

    @step
    def start(self):
        from sklearn import datasets
        from sklearn.model_selection import train_test_split
        self.iris = datasets.load_iris()
        self.X = self.iris['data']
        self.y = self.iris['target']
        self.labels = self.iris['target_names']
        self.next(self.model)

    @step
    def model(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        clf = RandomForestClassifier(n_estimators=10, 
                                     max_depth=None,
                                     min_samples_split=2,
                                     random_state=0)
        self.scores = cross_val_score(clf, self.X, 
                                      self.y, cv=3)
        self.next(self.end)
    
    @step
    def end(self):
        print(self.scores)
        print("TrackedFlow is all done.")

if __name__ == "__main__":
    wandb.init(mode="offline")
    TrackedFlow()
