---
published: false
layout: post
title: Kubernetes, Develop Helm Charts
tags: kubernetes kubectl ingress security phc.txn2.net
featured: kubernetes cli
mast: helm
---

Helm is the official Kubernetes package manager.


## Resources

If you found this article useful, you may want to check out all the articles used to build on the [Production Hobby Cluster].

- [phc.txn2.net]
- 


---

If in a few days you find yourself setting up a cluster in Japan or Germany on [Linode], and another two in Australia and France on [vultr], then you may have just joined the PHC (Performance [Hobby Cluster]s) club. Some people tinker late at night on their truck, we benchmark and test the resilience of node failures on our overseas, budget kubernetes clusters. It's all about going big, on the cheap.

[![k8s performance hobby clusters](https://github.com/cjimti/mk/raw/master/images/content/k8s-tshirt-banner.jpg)](https://amzn.to/2IOe8Yu)

[Ingress Nginx Auth Examples]: https://github.com/kubernetes/ingress-nginx/tree/master/docs/examples/auth
[phc.txn2.net]: http://localhost:4000/tag/phc.txn2.net/
[generic]: https://kubernetes-v1-4.github.io/docs/user-guide/kubectl/kubectl_create_secret_generic/
[kubectl create secret]: https://kubernetes-v1-4.github.io/docs/user-guide/kubectl/kubectl_create_secret/
[htpasswd]: https://httpd.apache.org/docs/current/programs/htpasswd.html
[Let's Encrypt, Kubernetes]: https://mk.imti.co/lets-encrypt-kubernetes/
[base64]: https://en.wikipedia.org/wiki/Base64
[Basic Auth]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication
[OAuth 2]: https://oauth.net/2/
[JWT]: https://jwt.io/
[Ingress]: https://mk.imti.co/web-cluster-ingress/
[Production Hobby Cluster]: https://mk.imti.co/hobby-cluster/
[Let's Encrypt]: https://letsencrypt.org/
[Hobby Cluster]: https://mk.imti.co/hobby-cluster/
[Linode]: https://www.linode.com/?r=848a6b0b21dc8edd33124f05ec8f99207ccddfde
[vultr]: https://www.vultr.com/?ref=7418713
[Secret]: https://kubernetes.io/docs/concepts/configuration/secret/
[ok]: https://github.com/txn2/ok