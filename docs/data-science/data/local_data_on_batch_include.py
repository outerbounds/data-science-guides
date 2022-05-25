from metaflow import FlowSpec, step, IncludeFile, batch

class IncludeFileFlow(FlowSpec):
    data = IncludeFile('data', 
                       default='./local_data.csv')

    @batch(cpu=1)
    @step
    def start(self):
        print(self.data)
        self.next(self.end)

    @step
    def end(self):
        print('Finished reading the data!')

if __name__ == '__main__':
    IncludeFileFlow()
