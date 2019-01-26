import yaml
import collections

from karavelcli import parser

def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

class ValuesObj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [ValuesObj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, ValuesObj(b) if isinstance(b, dict) else b)

class Values(object):
    def __init__(self, parser=parser):
        super(Values, self).__init__()
        self.parser = parser()
        self.values_dict = {}
        self.values = None
        self.init()

    def init(self):
        args = self.parser.parse_args()
        for fname in args.values:
            try:
                with open(fname) as f:
                    values_dict = yaml.load(f.read())
                dict_merge(self.values_dict, values_dict)
            except FileNotFoundError:
                print('Values file not found')
                raise FileNotFoundError

        self.values = ValuesObj(self.values_dict)
