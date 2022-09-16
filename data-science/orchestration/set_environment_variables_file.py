from metaflow import FlowSpec, step, batch
#highlight-next-line
from dotenv import load_dotenv
import os

IMAGE = "public.ecr.aws/outerbounds/dotenv:latest"

class EnvVarFlow(FlowSpec):
    
    @step
    def start(self):
        self.next(self.read_locally, self.read_in_container)
        
    @step
    def read_locally(self):
        secret = os.getenv("SUPER_DUPER_SECRET")
        print(f"secret message: {secret} " + \ 
               "from local environment")
        self.next(self.join)
        
    @batch(image=IMAGE, cpu=1)
    @step 
    def read_in_container(self):
        secret = os.getenv('SUPER_DUPER_SECRET')
        print(f"secret message: {secret} " + \ 
               "from a container")
        self.next(self.join)
        
    @step
    def join(self, inputs):
        self.next(self.end)
        
    @step
    def end(self):
        pass
        
if __name__ == "__main__":
    #highlight-next-line
    load_dotenv()
    EnvVarFlow()
