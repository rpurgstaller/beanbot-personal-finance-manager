from collections import defaultdict


class KeyValueMixin:

    type_conversion = defaultdict(
        lambda v: v, 
        {
            'int' : lambda v: int(v),
            'float' : lambda v: float(v),
            'str' : lambda v: v
        })

    def get_value(self):
        return self.type_conversion[self.value_type](self.value)