---
published: true
layout: post
title: kubectl Configuration
tags: kubernetes kubectl minikube cli
featured: kubernetes cli
mast: taylor
---

I work with four different Kubernetes clusters, a minikube on my local workstation, two test clusters and a production cluster. However, all my interaction with these clusters is done through a single utility on my mac: kubectl.

There are many ways to configure kubectl, from one config file to many and everywhere in between. To keep life less complicated I simply use one config file, found at its default location in the .kube folder in my home directory (`~/.kube/config`). The environment variable KUBECONFIG holds colon-separated paths to kubectl config files. If your KUBECONFIG is empty (`echo $KUBECONFIG`), like mine, you are using the default `~/.kube/config`.

The config file, `~/.kube/config` has three sections I care about:
-  `clusters`
-  `users`
-  and `contexts`

### Clusters

The clusters key in the configuration yaml contains a collection of cluster objects. Each cluster object is defined by a name, server, and certificate-authority. In this example, I name my dev cluster **exampledev**. [Certificates] are generated when setting up a cluster.

```yaml
clusters:
- cluster:
    certificate-authority: /Users/me/.kube/dev.crt
    server: https://kubeadm1.dev.example.com:6443
  name: exampledev
```
Minikube stores it configuration and certs in the `/Users/me/.minikube/` folder and specifically it's cert at the path 	`/Users/enochroot/.minikube/ca.crt`. The kubectl config for the minikube cluster looks like this:

```yaml
- cluster:
    certificate-authority: /Users/me/.minikube/ca.crt
    server: https://192.168.99.100:8443
  name: minikube
```



[Certificates]:https://kubernetes.io/docs/concepts/cluster-administration/certificates/