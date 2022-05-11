
from metaflow import FlowSpec, step

class ArtFlow(FlowSpec):

    @step
    def start(self):
        #highlight-next-line
        self.some_data = [1,2,3]
        self.next(self.middle)
        
    @step 
    def middle(self):
        #highlight-next-line
        print(f'the data artifact is: {self.some_data}')
        self.next(self.end)

    @step
    def end(self):
        #highlight-next-line
        print(f'the data artifact is still: {self.some_data}')
        pass

if __name__ == '__main__':
    ArtFlow()
