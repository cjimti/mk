---
published: false
layout: post
title: Let's Encrypt, Kubernetes
tags: kubernetes kubectl helm cli
featured: kubernetes cli
mast: helm
---

Use [cert-manager] to get port 443/https running with signed x509 certificates for [Ingress] on your Kubernetes [Production Hobby Cluster]. [cert-manager] is the successor to **kube-lego** and the prefered way to "[automatically obtain a browser-trusted certificates, without any human intervention.](https://letsencrypt.org/how-it-works/)" using [Let's Encrypt].

You will need to [install Helm] first if you do not already have it. If not checkout my article [Helm on Custom Kubernetes] expecially if you are following along with my [Production Hobby Cluster] guides.

### Install [cert-manager]

```bash
helm install --name cert-manager --namespace kube-system stable/cert-manager
```

After [Helm] installs [cert-manager] you end up with a [ServiceAccount] [ClusterRole], [ClusterRoleBinding], [Deployment] and a couple of [Pod]s named **cert-manager-cert-manager** in the **kube-system** [namespace]. [Helm] additionaly installs three [CustomResourceDefinition]s for [cert-manager] (custom resources are not namespaced):

- certificates.certmanager.k8s.io
- clusterissuers.certmanager.k8s.io
- issuers.certmanager.k8s.io

Although it's more information than you need right now, it's good to know what [Helm] installed for [cert-manager].

[cert-manager] uses ether an [Issuer] or [ClusterIssuer] to represent a certificate authority. [Issuer] is bound to a [namespace] so for our [Production Hobby Cluster] we will use a [ClusterIssuer].

We will setup a **letsencrypt-staging** and a **letsencrypt-prod** [ClusterIssuer].

### Create a [ClusterIssuer]

First we need to have a functional [Ingress] on our Kubernetes cluster. If you have not done so, check out my article [Ingress on Custom Kubernetes].

Create a file called `10-cluster-issuer-letsencrypt-staging.yml` for the [ClusterIssuer], add the following configuration and change the email address to your own.

```yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
  namespace: default
spec:
  acme:
    # The ACME server URL
    server: https://acme-staging.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: example@gmail.com
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-staging
    # Enable the HTTP-01 challenge provider
    http01: {}
```

Create the [ClusterIssuer] with `kubectl`:
```bash
kubectl create -f 10-cluster-issuer-letsencrypt-staging.yml
```

Expect output similar to the following:

```bash
clusterissuer.certmanager.k8s.io "letsencrypt-staging" created
```

```bash
kubectl describe ClusterIssuer
```

---

If in a few days you find yourself setting up a cluster in Japan or Germany on [Linode], and another two in Australia and France on [vultr], then you may have just joined the PHC (Performance [Hobby Cluster]s) club. Some people tinker late at night on their truck, we benchmark and test the resilience of node failures on our overseas, budget kubernetes clusters. It's all about going big, on the cheap.

[![k8s performance hobby clusters](https://github.com/cjimti/mk/raw/master/images/content/k8s-tshirt-banner.jpg)](https://amzn.to/2wzP4mg)

[Helm on Custom Kubernetes]: https://mk.imti.co/helm-on-custom-cluster/
[install Helm]: https://mk.imti.co/helm-on-custom-cluster/
[Ingress]: https://mk.imti.co/web-cluster-ingress/
[cert-manager]: https://github.com/jetstack/cert-manager/
[Production Hobby Cluster]: https://mk.imti.co/hobby-cluster/
[Let's Encrypt]: https://letsencrypt.org/
[Hobby Cluster]: https://mk.imti.co/hobby-cluster/
[Linode]: https://www.linode.com/?r=848a6b0b21dc8edd33124f05ec8f99207ccddfde
[vultr]: https://www.vultr.com/?ref=7418713
[Helm]: https://helm.sh/
[Pod]: https://kubernetes.io/docs/concepts/workloads/pods/pod/
[Deployment]: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
[ServiceAccount]: https://kubernetes.io/docs/admin/service-accounts-admin/
[ClusterRole]: https://kubernetes.io/docs/admin/authorization/rbac/#role-and-clusterrole
[ClusterRoleBinding]: https://kubernetes.io/docs/admin/authorization/rbac/#rolebinding-and-clusterrolebinding
[namespace]: https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
[CustomResourceDefinition]: https://kubernetes.io/docs/tasks/access-kubernetes-api/extend-api-custom-resource-definitions/
[ClusterIssuer]: https://cert-manager.readthedocs.io/en/latest/reference/clusterissuers.html
[Issuer]: https://cert-manager.readthedocs.io/en/latest/reference/issuers.html
[Certificates]: https://cert-manager.readthedocs.io/en/latest/reference/certificates.html
[Ingress on Custom Kubernetes]: https://mk.imti.co/web-cluster-ingress/