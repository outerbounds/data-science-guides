from metaflow import Parameter

def parameterize_flow():
    
    param_a = Parameter("a", default = 11)
    param_b = Parameter("b", default = 77)
    return param_a, param_b
