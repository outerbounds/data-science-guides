from metaflow import FlowSpec, step

class JoinArtifacts(FlowSpec):

    @step
    def start(self):
        self.pre_branch_data = 0
        self.next(self.branch_a, self.branch_b)
        
    @step
    def branch_a(self):
        self.x = 1 # define x 
        self.a = "a"
        self.next(self.join)
        
    @step
    def branch_b(self):
        self.x = 2 # define another x! 
        self.b = "b"
        self.next(self.join)
    
    @step
    def join(self, inputs):
        # pick which x to propagate
        self.x = inputs.branch_a.x 
        self.merge_artifacts(inputs, exclude=["a"])
        self.next(self.end)
        
    @step 
    def end(self):
        print("`pre_branch_data` " + \
              f"value is: {self.pre_branch_data}.")
        print(f"`x` value is: {self.x}.")
        print(f"`b` value is: {self.b}.")
        try: 
            print(f"`a` value is: {self.a}.")
        except AttributeError as e:
            print("`a` was excluded! \U0001F632")
        

if __name__ == "__main__":
    JoinArtifacts()
