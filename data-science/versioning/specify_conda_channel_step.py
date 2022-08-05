from metaflow import FlowSpec, step, conda

class SpecifyChannelsStep(FlowSpec):
    
    @step
    def start(self):
        self.next(self.make_pytorch_model)
    
    #highlight-next-line
    @conda(libraries={"pytorch::pytorch": "1.11.0"})
    @step 
    def make_pytorch_model(self):
        import torch
        self.next(self.end)
        
    @step
    def end(self):
        pass
        
if __name__ == "__main__":
    SpecifyChannelsStep()
