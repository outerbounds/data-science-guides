from metaflow import FlowSpec, step, Parameter

class ListStringParamFlow(FlowSpec):
    
    # highlight-next-line
    my_values = Parameter("vals", default = '1,2,3', separator = ',')
    
    @step
    def start(self):
        self.int_data = list(map(int, self.my_values))
        self.next(self.end)
        
    @step
    def end(self):
        print(self.int_data)

if __name__ == "__main__":
    ListStringParamFlow()
