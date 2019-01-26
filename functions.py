import os
import yaml
import tarfile
import importlib.util
from yaml import CLoader
from urllib.request import urlopen, urlretrieve

from kubernetes.client import ApiClient

def urljoin(*args):
    return '/'.join(map(lambda x: str(x).rstrip('/'), args))

def template_chart(args):
    current_dir = os.getcwd()
    chart_dir = os.path.join(current_dir, args.chart[0])
    api = ApiClient()
    templates = []
    fnames = []
    try:
        templates_dir = os.path.join(chart_dir, 'templates')
        for fname in os.listdir(templates_dir):
            full_path = os.path.join(templates_dir, fname)
            if os.path.isfile(full_path):
                parts = os.path.splitext(fname)
                if parts[1] == '.py':
                    tname = parts[0]
                    spec = importlib.util.spec_from_file_location(tname, full_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    t = mod.template()
                    if not isinstance(t, (list,tuple)):
                        t = [t]
                    templates.extend(t)
                    fnames += [full_path] * len(t)
        t_sanitized = api.sanitize_for_serialization(templates)
        output = '\n'.join([
            '---\n{}\n{}'.format(
                '# Source: {}'.format(os.path.relpath(fname ,current_dir)),
                yaml.dump(t, default_flow_style=False)
            )
            for t, fname in zip(t_sanitized, fnames)
        ])
    except FileNotFoundError:
        pass
    print(output)

def ensure(args):
    current_dir = os.getcwd()
    chart_dir = os.path.join(current_dir, args.chart[0])
    try:
        fname = os.path.join(chart_dir, 'requirements.yaml')
        with open(fname) as f:
            deps = yaml.load(f.read()).get('dependencies')

        for dep in deps:
            name = dep.get('name')
            url = urljoin(dep.get('repository'), 'index.yaml')
            index_raw = urlopen(url).read()
            index = yaml.load(index_raw, Loader=CLoader)
            chart = index.get('entries').get(name)
            chart_url = None
            for entry in chart:
                if entry.get('version') == dep.get('version'):
                    chart_url = entry.get('urls')[0]
            if not chart_url:
                raise Exception('chart not found')

        file_tmp = urlretrieve(chart_url, filename=None)[0]
        base_name = os.path.basename(chart_url)
        file_name, file_extension = os.path.splitext(base_name)
        tar = tarfile.open(file_tmp)
        dir = os.path.join(chart_dir, 'dependencies', file_name)
        tar.extractall(path=dir)

    except FileNotFoundError:
        print('No templates directory found')
