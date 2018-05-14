---
published: false
layout: post
title: Ingress on Kubernetes using Traefik
tags: kubernetes kubectl cli
featured: kubernetes cli
mast: webcluster
---

There are more than a handful of ways to set up [ingress] on a custom Kubernetes cluster. I have become a huge fan of [Traefik], and not just because it is written in [go](https://golang.org/), well maybe a little, but that should'nt matter right? [Traefik] does a lot more than just [ingress] on [Kubernetes]

If you are looking to experiment or learn on a non-production cluster, I suggest you check out my previous article [Production Hobby Cluster], a step-by-step guide for setting up a custom production capable Kubernetes cluster.

### ClusterRoleBinding

<script src="https://gist.github.com/cjimti/5217849dc0d1b614256cbb126b20b2f8.js"></script>

```bash
kubectl apply -f https://gist.githubusercontent.com/cjimti/5217849dc0d1b614256cbb126b20b2f8/raw/c50581a7548e67b2d3cc463a000a18afa3a08870/traefik-rbac.yaml
```

### Deployment

<script src="https://gist.github.com/cjimti/5a2d1bbf6f9b208d1a61d9a64c18dea1.js"></script>

```bash
kubectl apply -f https://gist.githubusercontent.com/cjimti/5a2d1bbf6f9b208d1a61d9a64c18dea1/raw/74d9139ad0db3654d8cd3886edfdce6c78d5b221/deployment-service.yml
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
