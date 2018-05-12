---
published: true
layout: post
title: Hobby Web Cluster
tags: kubernetes kubectl cli
featured: kubernetes cli
mast: cluster
---

Setting up [ingress] on a custom Kubernetes cluster involves applying a small handfull of configurations. Follow the [deploy ingress] steps.

#### Setup a Namespace (ingress-nginx):
<script src="https://gist.github.com/cjimti/51ffb8c8e9595137cf8776900de1d484.js"></script>

Apply the configuration:

```bash
curl -L https://git.io/vpSgo | kubectl apply -f -
```

#### Setup a Default Backend (ingress-nginx):

<script src="https://gist.github.com/cjimti/14593af14725dfd86314091196bce2f1.js"></script>


```bash
curl -L https://git.io/vpSaG | kubectl apply -f -
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
