from metaflow import FlowSpec, step, current

class TeamCollabFlow(FlowSpec):
    
    @step
    def start(self):
        print("current.username: {}".format(current.username))
        print("current.namespace: {}".format(current.namespace))
        self.next(self.end)
        
    @step
    def end(self):
        import random
        self.choice = random.choice([1,2,3,4,5])
        print("Random choice was {}".format(self.choice))
    
if __name__ == "__main__":
    TeamCollabFlow()
