---
published: false
layout: post
title: Elasticsearch on Kubernetes
tags: kubernetes
featured: kubernetes
mast: es
---

Installing production ready, EElasticsearch 6.2 on Kubernetes requires a hand full of simple configurations. The following guide is a high level overview of an installation process using Elastic's [recommendations for best practices]. The Github project [kubernetes-elasticsearch-cluster] is used for the Elastic Docker container and built for the purpose of operating Elasticsearch with nodes dedicated as Master, Data and Ingest.

The Docker container [docker-elasticsearch], a "Ready to use, lean and highly configurable Elasticsearch container image." by [pires] is sufficent for use in this guide, however, the [txn2/k8s-es] wraps it with a few minor preset environment variables to simplfy configuration. The docker image [txn2/k8s-es:v6.2.3] is used below.

The Github repository [kubernetes-elasticsearch-cluster] contains detailed documentation and configuration for using [docker-elasticsearch] with Kubernetes.

If you need to setup a quick, yet custom production grade cluster, checkout my article [Production Hobby Cluster] to get you started.

**Quick Reference:**

* Do not remove this line (for toc on a rendered blog)
{:toc}

### Namespace

In the examples below I'll use the namespace **the-project** for all the configurations. The file names are suggestions and should be named to your standards.

`00-namespace.yml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: the-project
  labels:
    env: dev
```

Create the namespace:
```bash
kubectl create -f 00-namespace.yml
```

### Access and Security - RBAC

Your Kubernetes cluster should be setup to use RBAC. If you are just getting started, you may want to setup a [permissive RBAC] implementation for your development cluster.

We begin by creating a [ServiceAccount] called `sa-elasticsearch` for Elasticsearch in `the-project` namespace.

```bash
kubectl create serviceaccount sa-elasticsearch -n the-project
```

Next, create a [Role and RoleBinding] for the new `sa-elasticsearch` [ServiceAccount], it makes sense to group tease in the same configuration file.

`10-rbac.yml`
```yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: elasticsearch
  namespace: the-project
  labels:
    env: dev
rules:
- apiGroups:
  - ""
  resources:
  - endpoints
  verbs:
  - get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: elasticsearch
  namespace: the-project
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: elasticsearch
subjects:
- kind: ServiceAccount
  name: sa-elasticsearch
  namespace: the-project
```

Create the [Role and RoleBinding]:
```bash
kubectl create -f 10-rbac.yml
```

### Services

You need  Kubernetes [Services] for each of the Elasticsearch node types, Master, Data and Ingest. [Services] are the persistant communication bridge to a [Pod]. Because Services use [selectors] to find the appropriate [Pod] they can be setup first. [Services] are accustomed to Pods comming and going, and will route to them when they are available, as they will be once we add Deployments further down.

Combine all three Services in the same configuration file to keep things simple.

`20-services.yml`:
```yaml
---
apiVersion: v1
kind: Service
metadata:
  namespace: the-project 
  name: elasticsearch
  labels:
    env: dev
spec:
  type: ClusterIP
  selector:
    app: elasticsearch
    role: client
  ports:
  - name: http
    port: 9200
    protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  namespace: the-project 
  name: elasticsearch-data
  labels:
    env: dev
spec:
  ports:
  - port: 9300
    name: transport
  clusterIP: None
  selector:
    app: elasticsearch
    role: data
---
apiVersion: v1
kind: Service
metadata:
  namespace: the-project 
  name: elasticsearch-discovery
  labels:
    env: dev
spec:
  selector:
    app: elasticsearch
    role: master
  ports:
  - name: transport
    port: 9300
    protocol: TCP
```


[recommendations for best practices]: https://www.elastic.co/guide/en/elasticsearch/reference/6.2/modules-node.html
[kubernetes-elasticsearch-cluster]: https://github.com/pires/kubernetes-elasticsearch-cluster
[txn2/k8s-es]:https://github.com/txn2/k8s-es
[txn2/k8s-es:v6.2.3]:https://hub.docker.com/r/txn2/k8s-es/tags/
[issues]: https://github.com/pires/kubernetes-elasticsearch-cluster/issues
[pires]:https://github.com/pires
[docker-elasticsearch]:https://github.com/pires/docker-elasticsearch
[permissive RBAC]:https://mk.imti.co/hobby-cluster/#permissions-rbac-role-based-access-control
[Production Hobby Cluster]:https://mk.imti.co/hobby-cluster/
[ServiceAccount]:http://localhost:4000/team-kubernetes-remote-access/#serviceaccount
[Role and RoleBinding]:http://localhost:4000/team-kubernetes-remote-access/#role-and-rolebinding
[Services]:https://kubernetes.io/docs/concepts/services-networking/service/
[Pod]:https://kubernetes.io/docs/concepts/workloads/pods/pod/
[selectors]:https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/