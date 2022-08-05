 
class MyFlow(FlowSpec):

    @step
    def start(self):
        from my_module import do_logic
        do_logic()
        self.next(self.next_step)
    
    # rest of flow
