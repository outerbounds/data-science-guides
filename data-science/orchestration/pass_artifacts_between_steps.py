
from metaflow import FlowSpec, step

class ArtFlow(FlowSpec):

    @step
    def start(self):
        #highlight-next-line
        self.some_data = [1,2,3] # define artifact state
        self.next(self.middle)
        
    @step 
    def middle(self):
        #highlight-next-line
        print(f'the data artifact is: {self.some_data}')
        self.some_data = [1,2,4] # update artifact state
        self.next(self.end)

    @step
    def end(self):
        #highlight-next-line
        print(f'the data artifact is: {self.some_data}')

if __name__ == '__main__':
    ArtFlow()
