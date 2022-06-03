from metaflow import FlowSpec, step, batch, environment
import os

IMAGE = 'public.ecr.aws/docker/library/' + \
        'python:3.9.12-buster'

class EnvVarFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.read_locally, 
                  self.read_in_container)

    #highlight-start
    @environment(vars={
        "STEP_VAR": f"{os.getenv('MSG')} from local"})
    #highlight-end
    @step
    def read_locally(self):
        print(f"secret message: {os.getenv('STEP_VAR')}")
        self.next(self.join)
        
    #highlight-start
    @environment(vars = 
        {"STEP_VAR": f"{os.getenv('MSG')} from container"})
    #highlight-end
    @batch(image=IMAGE, 
           cpu=1)
    @step 
    def read_in_container(self):
        print(f"secret message: {os.getenv('STEP_VAR')}")
        self.next(self.join)
        
    @step
    def join(self, inputs):
        self.next(self.end)
        
    @step
    def end(self):
        pass
        
if __name__ == "__main__":
    EnvVarFlow()
