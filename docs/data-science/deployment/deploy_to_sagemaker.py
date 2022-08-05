
from metaflow import FlowSpec, step, S3, conda_base
import os
import json

class DeployToSagemakerFlow(FlowSpec):
    
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
        self.next(self.train_rf_model)
        
    @step
    def train_rf_model(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        self.clf = RandomForestClassifier(random_state=0)
        self.clf.fit(self.X_train, self.y_train)
        # will use local preds as test of `deploy` step.
        self.local_y_pred = self.clf.predict(self.X_test)
        self.next(self.deploy)

    @step
    def deploy(self):
        import time
        import deployer 
        t = int(round(time.time() * 1000))
        self.sagemaker_model_name = 'rf-model-{}'.format(t)
        self.model_save_name = 'model'
        self.endpoint_name = 'rf-endpoint-{}'.format(t)
        self.instance_type = 'ml.c5.2xlarge'
        self.entry_point = 'sagemaker_entry_point.py'
        self.sklearn_sage_version = '1.0-1'
        self.model_s3_path = deployer.to_sagemaker(
            model = self.clf,
            sagemaker_model_name = self.sagemaker_model_name,
            model_save_name = self.model_save_name,
            endpoint_name = self.endpoint_name, 
            instance_type = self.instance_type, 
            entry_point = self.entry_point,
            sklearn_version = self.sklearn_sage_version,
            role = os.getenv('ROLE'), 
            code_location=os.getenv('CODE_LOCATION'),
            run = self
        )
        self.next(self.end)

    @step
    def end(self):
        print("\nModel name is: {}".format(
            self.sagemaker_model_name))
        print("Endpoint name is: {}\n".format(
            self.endpoint_name))

if __name__ == "__main__":
    DeployToSagemakerFlow()
