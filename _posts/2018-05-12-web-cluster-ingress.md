---
published: false
layout: post
title: Hobby Web Cluster
tags: kubernetes kubectl cli
featured: kubernetes cli
mast: webcluster
---

Setting up [ingress] on a custom Kubernetes cluster involves applying a small handful of configurations. Follow the [deploy ingress] steps from the source repository, or follow along below.

If you are looking to experiment or learn on a non-production cluster, I suggest you check out my previous article [Production Hobby Cluster](/hobby-cluster/), a step-by-step guide for setting up a custom production capable Kubernetes cluster.

#### Setup a Namespace (ingress-nginx):
<script src="https://gist.github.com/cjimti/51ffb8c8e9595137cf8776900de1d484.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSgo | kubectl apply -f -
```

#### Setup a Default Backend (ingress-nginx):

Next, setup a default backend, where any traffic goes when the ingress controller does not have a matching configuration for the request. The new default backend is called `default-http-backend` and is deployed under the new `ingress-nginx` namespace.

The following configuration consists of a deployment creating a pod from the `gcr.io/google_containers/defaultbackend:1.4` docker image with port 8080 exposed, along with a corresponding service exposing port 80 and connecting it with port 8080 on the pod.

<script src="https://gist.github.com/cjimti/14593af14725dfd86314091196bce2f1.js"></script>


```bash
curl -L https://git.io/vpSaG | kubectl apply -f -
```

#### Setup a ConfigMap for Ingress

The following stubs out an empty ConfigMap for ingress.

<script src="https://gist.github.com/cjimti/cdfb2b7ba7ce9b26d9741eed843e8fb0.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSQv | kubectl apply -f -
```

#### Setup a TCP Services ConfigMap for Ingress

The following stubs out an empty ConfigMap for ingress TCP services.

<script src="https://gist.github.com/cjimti/d2aa74284684b2ffe8570dae1b80b460.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSQL | kubectl apply -f -
```

#### Setup a UDP Services ConfigMap for Ingress

The following stubs out an empty ConfigMap for ingress UDP services.

<script src="https://gist.github.com/cjimti/cdfb2b7ba7ce9b26d9741eed843e8fb0.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSxA | kubectl apply -f -
```

#### Install with [RBAC] roles

If you followed along with my article [Production Hobby Cluster] you already running with [RBAC].

The following configuration adds a [ServiceAccount] named `nginx-ingress-serviceaccount`, a [ClusterRole] named `nginx-ingress-clusterrole` a RoleBinding and a ClusterRoleBinding to tie it all together.

<script src="https://gist.github.com/cjimti/957c550dab0bbbdd7b5efb765b8240a7.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSpO | kubectl apply -f -
```

#### Deployment

Next we have the deployment configuration managing a pod with the ingress nginx image `quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.14.0`.

<script src="https://gist.github.com/cjimti/e3dde45167d407aba96375044570b426.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSpW | kubectl apply -f -
```

#### ingress-nginx Service (Baremetal / NodePort)

We are running a custom cluster on a vendor neutral platform (No AWS or Azure here) so don't get to take advantage of build in load balancing, but we will get to that in another post.

The following `ingress-nginx` service sets up a service pointing to port 80 and port 443 of our nginx controller. Using NodePort without specifying a port will let the cluster assign one for us.

<script src="https://gist.github.com/cjimti/c49921ff714153ed7367769fb9d89670.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSpQ | kubectl apply -f -
```

#### Verify Installation

```bash
kubectl get all --all-namespaces -l app=ingress-nginx

NAMESPACE       NAME                                           READY     STATUS    RESTARTS   AGE
ingress-nginx   pod/nginx-ingress-controller-9fbd7596d-5hdj8   1/1       Running   0          35m

NAMESPACE       NAME                                       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
ingress-nginx   deployment.apps/nginx-ingress-controller   1         1         1            1           35m

NAMESPACE       NAME                                                 DESIRED   CURRENT   READY     AGE
ingress-nginx   replicaset.apps/nginx-ingress-controller-9fbd7596d   1         1         1         35m
```




If in a few days you find yourself setting up a cluster in Japan or Germany on [Linode], and another two in Australia and France on [vultr], then you may have just joined the PHC (Performance Hobby Clusters) club. Some people tinker late at night on their truck, we benchmark and test the resilience of node failures on our overseas, budget kubernetes clusters. It's all about going big, on the cheap.

[![k8s performance hobby clusters](https://github.com/cjimti/mk/raw/master/images/content/k8s-tshirt-banner.jpg)](https://amzn.to/2wzP4mg)




## Resources

- [deploy ingress]
- [ingress]
- [Linode]
- [Digital Ocean]
- [Vultr]
- [KUBECONFIG]
- [systemd]
- [Weave Net]
- [Etcd]
- [WireGuard]
- [Hobby Kube] A fantastic write-up (with teraform scripts) and how I got started.

[ServiceAccount]: https://kubernetes.io/docs/admin/service-accounts-admin/
[RBAC]: https://github.com/kubernetes/ingress-nginx/blob/master/docs/deploy/rbac.md
[Production Hobby Cluster]: /hobby-cluster/
[deploy ingress]: https://github.com/kubernetes/ingress-nginx/blob/master/docs/deploy/index.md
[ingress]: https://github.com/kubernetes/ingress-nginx
[Linode]: https://www.linode.com/?r=848a6b0b21dc8edd33124f05ec8f99207ccddfde
[Digital Ocean]: https://m.do.co/c/97b733e7eba4
[vultr]: https://www.vultr.com/?ref=7418713
[KUBECONFIG]: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/
[systemd]: https://wiki.ubuntu.com/systemd
[WireGuard]: https://www.wireguard.io/
[Weave Net]: https://www.weave.works/oss/net/
[Etcd]: https://coreos.com/etcd/docs/latest/getting-started-with-etcd.html
[Hobby Kube]: https://github.com/hobby-kube/guide
