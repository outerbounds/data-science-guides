from metaflow import FlowSpec, step

class ListStepsFlow(FlowSpec):
    
    @step
    def start(self):
        self.art = 1
        self.next(self.a)
    
    @step
    def a(self):
        self.art = 2
        self.next(self.b)
        
    @step
    def b(self):
        self.art = 3
        self.next(self.c)
        
    @step
    def c(self):
        self.art = 5
        self.next(self.end)
        
    @step
    def end(self):
        pass
    
if __name__ == "__main__":
    ListStepsFlow()
