
from metaflow import FlowSpec, step

class FlowToTest(FlowSpec):

    @step
    def start(self):
        self.x = 0
        self.next(self.end)

    @step
    def end(self):
        self.x += 1

if __name__ == '__main__':
    FlowToTest()
