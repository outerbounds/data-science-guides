from metaflow import FlowSpec, step, Parameter

class ListMultipleParamFlow(FlowSpec):
    
    # highlight-next-line
    my_values = Parameter("val", default = 2, multiple = True)

    @step
    def start(self):
        self.next(self.end)
        
    @step
    def end(self):
        print(list(self.my_values))

if __name__ == "__main__":
    ListMultipleParamFlow()
