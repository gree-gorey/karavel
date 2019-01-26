from kubernetes import client

from karavel.helm import HelmChart
from karavel.helpers import Values

def template():
    values = Values().values
    # Initialize the chart (== helm template --values)
    chart = HelmChart(name='mysql', version='0.13.1', values=values.mysql.helm)
    # Get the desired object from chart
    service = chart.get(name='svc', obj_class=client.V1Service)
    # Create custom objects to add
    custom_ports = [
        client.V1ServicePort(
            name='my-custom-port',
            protocol=values.mysql.protocol,
            port=values.mysql.port,
            target_port=39000,
        )
    ]
    # Add custom objects to the service
    service.spec['ports'] = custom_ports
    # Change Helm-generated label
    service.metadata['labels']['release'] += '-suffix'
    # Delete Helm-generated label `heritage: Tiller`
    del service.metadata['labels']['heritage']

    return service # [service], (service, service) are valid
