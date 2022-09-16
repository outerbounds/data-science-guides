from metaflow import FlowSpec, step, Parameter
from shared_params import parameterize_flow

class ReuseParameters(FlowSpec):
    
    #highlight-next-line
    param_a, param_b = parameterize_flow()
    
    @step
    def start(self):
        self.next(self.end)
    
    @step
    def end(self):
        print("FlowA.param_a is {}".format(self.param_a))
        print("FlowA.param_b is {}".format(self.param_b))
    
if __name__ == "__main__":
    ReuseParameters()
