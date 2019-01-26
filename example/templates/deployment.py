from kubernetes import client

from karavel.helpers import Values

def template():
    values = Values().values
    # Configureate Pod template container
    container = client.V1Container(
        name='nginx',
        image='{}:{}'.format(values.nginx.image.repository, values.nginx.image.tag),
        ports=[client.V1ContainerPort(container_port=80)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={'app': 'nginx'}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=3,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version='extensions/v1beta1',
        kind='Deployment',
        metadata=client.V1ObjectMeta(name='nginx-deployment'),
        spec=spec)

    return deployment # [deployment], (deployment, deployment) are valid
