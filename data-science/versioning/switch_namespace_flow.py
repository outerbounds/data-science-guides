from metaflow import Flow, FlowSpec, step, namespace, get_namespace, current

def get_flow_data(flow, ns):
    namespace(ns)
    run = Flow(flow).latest_successful_run
    return run.data

class SwitchNamespaceFlow(FlowSpec):
    
    @step
    def start(self):
        print("{}".format(
            get_flow_data(
                flow='TeamCollabFlow', 
                ns=get_namespace()
            ).data
        ))
        self.next(self.end)
        
    @step
    def end(self):
        pass 
        
if __name__ == "__main__":
    SwitchNamespaceFlow()
    #print(get_result())
