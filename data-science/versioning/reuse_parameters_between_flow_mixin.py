from metaflow import FlowSpec, step, Parameter
from shared_params_and_functionality import FlowMixin

class FlowB(FlowSpec, FlowMixin):
    
    @step
    def start(self):
        self.next(self.end)
    
    @step
    def end(self):
        print(self.model_config)
    
if __name__ == "__main__":
    FlowB()
