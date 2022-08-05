from metaflow import FlowSpec, step, retry, catch

class CatchRetryFlow(FlowSpec):

    @step
    def start(self):
        self.divisors = [0, 1, 2]
        self.next(self.divide, foreach='divisors')

    #highlight-start
    @catch(var='divide_fail')
    @retry(times=1)
    #highlight-end
    @step
    def divide(self):
        #highlight-next-line
        self.res = 10 / self.input
        self.next(self.join)

    @step
    def join(self, inputs):
        #highlight-next-line
        self.results = [i.res 
                        for i in inputs 
                        if not i.divide_fail]
        print('results', self.results)
        self.next(self.end)

    @step
    def end(self):
        print('done!')

if __name__ == '__main__':
    CatchRetryFlow()
