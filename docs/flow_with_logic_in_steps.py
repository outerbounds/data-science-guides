
class MyFlow(FlowSpec):

    @step
    def start(self):
        # logic A
        # logic B 
        # logic C
        self.next(self.next_step)
        
    # rest of flow
