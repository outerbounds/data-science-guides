from metaflow import Parameter

class FlowMixin:

    param_a = Parameter("a", default = 11)
    param_b = Parameter("b", default = 77)

    @property
    def model_config(self):
        return {"a": self.param_a, "b": self.param_b}
