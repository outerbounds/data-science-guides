from metaflow import FlowSpec, step, environment, batch, conda_base
import os
import wandb
from wandb_helpers import plot_results
    
@conda_base(libraries={"wandb": "0.12.15", "scikit-learn": "1.0.2", 
                       "pandas": "1.4.2"})
class TrackPlotsFlow(FlowSpec):
    
    @step
    def start(self):
        from sklearn import datasets
        from sklearn.model_selection import train_test_split
        self.iris = datasets.load_iris()
        self.X = self.iris['data']
        self.y = self.iris['target']
        self.labels = self.iris['target_names']
        split = train_test_split(self.X, self.y, 
                                 test_size=0.2)
        self.X_train = split[0] 
        self.X_test = split[1]
        self.y_train = split[2]
        self.y_test = split[3]
        self.next(self.model)

    # Copy env vars to tasks on a different machine.
    @environment(vars={
        "WANDB_API_KEY": os.getenv("WANDB_API_KEY"), 
        "WANDB_NAME": "Plot RandomForestClassifier",
        "WANDB_ENTITY": os.getenv("WANDB_ENTITY"),
        "WANDB_PROJECT": os.getenv("WANDB_PROJECT")
    })
    @batch(cpu=2)
    @step
    def model(self):
        from sklearn.ensemble import RandomForestClassifier
        self.clf = RandomForestClassifier(
            n_estimators=10, max_depth=None,
            min_samples_split=2, random_state=0
        )
        from sklearn.model_selection import cross_val_score
        self.clf.fit(self.X_train, self.y_train)
        self.y_pred = self.clf.predict(self.X_test)
        self.y_probs = self.clf.predict_proba(
            self.X_test
        )
        #highlight-start
        plot_results(self.X_train, self.y_train, 
                     self.X_test, self.y_test, 
                     self.y_pred, self.y_probs, 
                     self.clf, self.labels)
        #highlight-end
        self.next(self.end)
    
    @step
    def end(self):
        print("Flow is all done.")

if __name__ == "__main__":
    TrackPlotsFlow()
