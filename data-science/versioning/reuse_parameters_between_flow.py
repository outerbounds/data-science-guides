from metaflow import FlowSpec, step, Parameter
from shared_params_and_functionality import FlowMixin

class FlowB(FlowSpec, FlowMixin):
    
    #highlight-next-line
    param_a, param_b = parameterize_flow()
    
    @step
    def start(self):
        self.next(self.end)
    
    @step
    def end(self):
        print(self.model_config)
    
if __name__ == "__main__":
    FlowA()
