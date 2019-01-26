import os
import yaml
import subprocess

from kubernetes import client
from kubernetes.client import ApiClient

class HelmChart(object):
    def __init__(self, name, version, values):
        super(HelmChart, self).__init__()
        self.name = name
        self.version = version
        self.values = values
        self.api = ApiClient()
        self.templates = {}
        self.init()

    def init(self):
        version = self.version
        dir = os.path.join('dependencies', 'temp')
        if not os.path.exists(dir):
            os.makedirs(dir)
        fvalues = os.path.join(dir, 'values.yaml')
        with open(fvalues, 'w') as f:
            yaml.dump(self.values, f, default_flow_style=False)
        p = subprocess.run(
            [
                'helm',
                'template',
                os.path.join(
                    'dependencies',
                    '{name}-{version}'.format(name=self.name, version=version),
                    self.name,
                ),
                '--values={}'.format(fvalues),
                '--output-dir={}'.format(dir),
                '--name={}'.format(self.values.releaseName),
                '--namespace={}'.format(self.values.namespace),
            ],
            stdout=open(os.devnull, 'w'),
        )
        templates_dir = os.path.join(dir, self.name, 'templates')
        for fname in os.listdir(templates_dir):
            tname = os.path.splitext(fname)[0]
            fullpath = os.path.join(templates_dir, fname)
            if os.path.isfile(fullpath):
                with open(fullpath) as f:
                    docs = yaml.load_all(f.read())
                    self.templates[tname] = [d for d in docs]

    def get(self, name, obj_class):
        obj_dict = self.templates[name][0]
        reversed_attrs = {v:k for k, v in obj_class.attribute_map.items()}
        obj_dict_sanitized = {reversed_attrs[k]:v for k, v in obj_dict.items()}
        obj = obj_class(**obj_dict_sanitized)

        return obj
