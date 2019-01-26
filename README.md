# karavel
Yet another Kubernates tempalting tool, Python-based

# Usage

```console
$ cd example
$ docker run -v $PWD:/chart greegorey/karavel ensure .
$ docker run -v $PWD:/chart greegorey/karavel template -f values.yaml -f prod.yaml .
---
# Source: templates/custom-resource.py
apiVersion: stable.example.com/v1
kind: Whale
metadata:
  name: my-object
spec:
  fins: 4
  image: my-whale-image:0.0.1
  tail: 1

---
# Source: templates/deployment.py
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:1.14-alpine
        name: nginx
        ports:
        - containerPort: 80

---
# Source: templates/service-helm.py
apiVersion: v1
kind: Service
metadata:
  annotations: null
  labels:
    app: prod-release-mysql
    chart: mysql-0.13.1
    release: prod-release-suffix
  name: prod-release-mysql
spec:
  ports:
  - name: my-custom-port
    port: 3308
    protocol: TCP
    targetPort: 39000
  selector:
    app: prod-release-mysql
  type: NodePort

```
