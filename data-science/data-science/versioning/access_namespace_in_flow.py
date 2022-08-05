from metaflow import (Flow, FlowSpec, step, namespace, 
                      default_namespace, Parameter)

def get_flow_data(flow, new_ns, original_ns=default_namespace()):
    try:
        namespace(new_ns)
        run = Flow(flow).latest_successful_run
    except:
        return
    namespace(original_ns)
    return run

class AccessOtherNamespace(FlowSpec):
    
    other_flow_name = Parameter('other-flow-name', 
                                default='TeamCollabFlow')
    other_namespace = Parameter('other-namespace',
                                default=default_namespace())
    msg = "{}.latest_successful_run.data. has value {}."
    
    @step
    def start(self):
        
        # access other_flow_name in other_namespace
        run = get_flow_data(
            flow = self.other_flow_name,
            new_ns = self.other_namespace
        )
        if run is None:
            print("Flow {} not found in {} namespace.".format(
                self.other_flow_name,
                self.other_namespace
            ))
        else:
            print(self.msg.format(
                self.other_flow_name,
                run.data.choice,
            ))
        self.next(self.end)
        
    @step
    def end(self):
        pass 
        
if __name__ == "__main__":
    AccessOtherNamespace()
