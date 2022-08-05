from metaflow import FlowSpec, step, batch, conda
import os

class UseImageFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.run_in_container)
    
    #highlight-next-line
    @batch(image="python:3.10-slim", cpu=1)
    @step 
    def run_in_container(self):
        self.artifact_from_container = 7
        self.next(self.end)
        
    @step
    def end(self):
        pass
        
if __name__ == "__main__":
    UseImageFlow()
