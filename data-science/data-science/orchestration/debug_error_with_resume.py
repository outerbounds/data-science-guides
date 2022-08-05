#meta:tag=hide
from metaflow import FlowSpec, step

class DebugFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.a, self.b)

    @step
    def a(self):
        self.x = 1
        self.next(self.join)

    @step
    def b(self):
        self.x = 0
        self.next(self.join)

    @step
    def join(self, inputs):
        # Fix bug.
        self.result = inputs.a.x / (inputs.b.x + 1e-12) 
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == '__main__':
    DebugFlow()
