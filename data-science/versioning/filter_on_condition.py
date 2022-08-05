from metaflow import FlowSpec, step

class ConditionalFilterFlow(FlowSpec):
    
    @step
    def start(self):
        import random
        self.fancy_conditional = random.choice([1,2,3])
        print(self.fancy_conditional)
        self.next(self.end)
        
    @step
    def end(self):
        pass
    
if __name__ == "__main__":
    ConditionalFilterFlow()
