from metaflow import FlowSpec, step, conda_base

#highlight-start
@conda_base(libraries={"pytorch::pytorch": "1.11.0", 
                       "boto3": "1.24.4"},
            python="3.8.0")
#highlight-end
class SpecifyChannelsFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.make_pytorch_model)
    
    @step 
    def make_pytorch_model(self):
        import torch
        import boto3
        self.next(self.end)
        
    @step
    def end(self):
        pass
        
if __name__ == "__main__":
    SpecifyChannelsFlow()
