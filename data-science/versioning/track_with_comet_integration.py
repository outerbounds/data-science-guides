
from comet_ml import init
from comet_ml.integration.metaflow import comet_flow
from metaflow import FlowSpec, JSONType, Parameter, card, step

#highlight-next-line
@comet_flow(project_name="comet-metaflow")
class CometFlow(FlowSpec):

    @step
    def start(self):
        import plotly.express as px
        from sklearn.model_selection import train_test_split
        self.input_df = px.data.tips()
        self.X = self.input_df.total_bill.values[:, None]
        self.X_train, self.X_test, \
        self.Y_train, self.Y_test = train_test_split(
            self.X, self.input_df.tip, random_state=42
        )
        self.next(self.train_model)

    @step
    def train_model(self):
        import numpy as np
        from sklearn import linear_model
        #highlight-next-line
        from comet_ml import API
        self.model = linear_model.LinearRegression()
        self.model.fit(self.X_train, self.Y_train)
        self.score = self.model.score(self.X_test, self.Y_test)
        #highlight-start 
        self.comet_experiment.log_parameter("model", self.model)
        self.comet_experiment.log_metric("score", self.score)
        #highlight-end
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    #highlight-next-line
    init()
    CometFlow()
