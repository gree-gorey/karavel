from kubernetes import client

def template():
    resource = {
        'apiVersion': 'stable.example.com/v1',
        'kind': 'Whale',
        'metadata': client.V1ObjectMeta(
            name='my-object',
        ),
        'spec': {
            'image': 'my-whale-image:0.0.1',
            'tail': 1,
            'fins': 4,
        }
    }

    return resource # [resource], (resource, resource) are valid
