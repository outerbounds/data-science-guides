from metaflow import FlowSpec, step, batch, conda
import os

class UseCUDAFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.run_in_container)
    
    #highlight-next-line
    @batch(image="nvcr.io/nvidia/rapidsai/rapidsai:22.06-cuda11.0-runtime-ubuntu18.04-py3.8", gpu=1)
    @step 
    def run_in_container(self):
        self.artifact_from_container = 7
        self.next(self.end)
        
    @step
    def end(self):
        pass
        
if __name__ == "__main__":
    UseCUDAFlow()
