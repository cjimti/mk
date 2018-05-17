---
published: true
layout: post
title: Ingress on Kubernetes using Traefik
tags: kubernetes kubectl cli
featured: kubernetes cli
mast: webcluster
---

There are more than a handful of ways to set up [ingress] on a custom Kubernetes cluster.

If you are looking to experiment or learn on a non-production cluster, I suggest you check out my previous article [Production Hobby Cluster], a step-by-step guide for setting up a custom production capable Kubernetes cluster.

This article builds on the [Production Hobby Cluster] and closely follows the [Traefik Kubernetes User Guide] and specifically the [DaemonSet] method.

### RBAC: Security and Permissions

ClusterRoleBinding:

<script src="https://gist.github.com/cjimti/5217849dc0d1b614256cbb126b20b2f8.js"></script>

```bash
kubectl apply -f https://gist.githubusercontent.com/cjimti/5217849dc0d1b614256cbb126b20b2f8/raw/c50581a7548e67b2d3cc463a000a18afa3a08870/traefik-rbac.yaml
```

### [DaemonSet]

This will ensure one [Traefik] pod will run on each node by configuring a `traefik-ingress-controller` [DaemonSet] in the `kube-system` namespace.

<script src="https://gist.github.com/cjimti/9c6c409c218cbd246167d58382068625.js"></script>

```bash
kubectl apply -f https://gist.githubusercontent.com/cjimti/9c6c409c218cbd246167d58382068625/raw/3c1190c4a1cae030b7dc417ee1aba25415fd1430/traefik-ds.yaml
```

Get the status of the [DaemonSet]:

```bash
kubectl get ds -n kube-system

NAME                         DESIRED   CURRENT   READY     UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
kube-proxy                   3         3         3         3            3           <none>          1d
traefik-ingress-controller   3         3         3         3            3           <none>          1m
weave-net                    3         3         3         3            3           <none>          1d
```

Get the status of the Pods:

```bash
kubectl get pods -n kube-system -l name=traefik-ingress-lb -o wide

NAME                               READY     STATUS    RESTARTS   AGE       IP               NODE
traefik-ingress-controller-fw2qq   1/1       Running   0          22h       149.28.77.205    la3
traefik-ingress-controller-g9mvb   1/1       Running   0          22h       45.77.71.39      la2
traefik-ingress-controller-ww25f   1/1       Running   2          22h       108.61.214.169   la1
```


If in a few days you find yourself setting up a cluster in Japan or Germany on [Linode], and another two in Australia and France on [vultr], then you may have just joined the PHC (Performance [Hobby Cluster]s) club. Some people tinker late at night on their truck, we benchmark and test the resilience of node failures on our overseas, budget kubernetes clusters. It's all about going big, on the cheap.

[![k8s performance hobby clusters](https://github.com/cjimti/mk/raw/master/images/content/k8s-tshirt-banner.jpg)](https://amzn.to/2wzP4mg)



## Resources

- Kubernetes [DaemonSet].
- [deploy ingress] on Kubernetes.
- Nginx [ingress] controller.
- [Linode] hosting.
- [Digital Ocean] hosting.
- [Vultr] hosting.
- Using [KUBECONFIG] for multiple configuration files.
- [systemd] help.
- [Weave Net] container networking.
- [Etcd] distributed keystore.
- [WireGuard] VPN.
- [Hobby Kube] A fantastic write-up (with teraform scripts) and how I got started.

[Kubernetes]: https://kubernetes.io/
[DaemonSet]: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
[Traefik Kubernetes User Guide]: https://docs.traefik.io/user-guide/kubernetes/
[Traefik]: https://traefik.io/
[Hobby Cluster]: https://mk.imti.co/hobby-cluster/
[Production Hobby Cluster]: https://mk.imti.co/hobby-cluster/
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
