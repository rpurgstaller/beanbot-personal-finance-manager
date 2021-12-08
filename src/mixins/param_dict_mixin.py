from collections import defaultdict


class ParamDictMixin:

    type_conversion = defaultdict(
        lambda v: v, 
        {
            'int' : lambda v: int(v),
            'float' : lambda v: float(v)
        })

    def init_on_load(self, param_dict):
        self.param_dict = param_dict

    def get_param(self, key):
        param = self.param_dict[key]
        return self.type_conversion[param.value_type](param.value)