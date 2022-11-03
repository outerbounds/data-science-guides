from metaflow import FlowSpec, step, Parameter
from sklearn_api import SklearnSupervisedClassifier

class PredictFlow(FlowSpec, SklearnSupervisedClassifier):

    #highlight-next-line
    sibling_flow = 'TrainFlow'
    str_data = Parameter(
        "data",
        default = '6.4,2.8,5.6,2.1',
        separator = ','
    )

    @step
    def start(self):
        # map data to expected type of 2d array
        raise NotImplementedError()
        self.data = [list(map(float, self.str_data))]
        self.next(self.make_prediction)

    @step
    def make_prediction(self):
        #highlight-start
        from metaflow import Flow
        run = Flow(self.sibling_flow).latest_successful_run
        self.model = run['end'].task.data.model
        self.prediction = self.predict(self.model, self.data)
        #highlight-end
        self.training_run_id = run.id
        self.next(self.end)

    @step
    def end(self):
        print("Finished PredictFlow!")

if __name__ == "__main__": 
    PredictFlow()
