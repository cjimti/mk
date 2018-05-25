---
published: false
layout: post
title: Kubernetes, Fission Serverless Application Platform
tags: kubernetes kubectl helm cli serverless lambda phc.txn2.net
featured: kubernetes cli
mast: fission
---

Fission is a new Kubernetes framework, where "[developers write functions that use Fission's API, much the same as they would for AWS Lambda.][Fission framework news]". **In this article I focus on installing [Fission] on top of my [Production Hobby Cluster]**, specifically due to it's out-of-the box support for [Go] and [Python3], two languages I am doing a lot of development in lately.

### Background

In my opinion, Amazon really kicked off the serverless movement into overdrive by teaching thousands of developers the power of [FaaS] with [Amazon Echo] development tutorials and workshops. I was one of them and I have the T-Shirt to prove it! I wrote a simple name generator called [Name Weasel] using [AWS Lambda].

While [vendor lock-in] is fine when you are developing services specifically for a product like [Amazon Echo] it starts to make less sense when developing a custom application or service. If you think about blogs and content sites, their value is in the content, using a platform service like Wordpress or SquareSpace makes some sense since the value is in the content, not the platform. However when you are developing a platform on a vendor platform, you are married to that vendor. I want to utilize and leverage many of Google and Amazon's services, I just don't want the core functionality of my system to be forever tied to them.

[Vendor neutral], [serverless] architectures are starting to mature, [OpenFaaS], [OpenWhisk], [kubeless], and [Fission]. We have even seen some projects come and go, like [funktion], but this is a good thing, to see different approaches that can really only be vetted by developing them and letting developers kick the tires. The best does not always win the lion share of community support, but what is best is not always intuative, best is subjective only to the context of the developer and stakeholders of the resulting development, regardless of the seemingly objective arguments of academeics and software pundits.

### Getting Started

You need to [install Helm] first if you do not already have it. Otherwise, check out my article [Helm on Custom Kubernetes], especially if you are following along with my [Production Hobby Cluster] guides.

Next, install [Fission] **0.7.2** using [helm] in the fission [namespace] using the the [Service] type [NodePort]:

```bash
helm install --namespace fission --set serviceType=NodePort,routerServiceType=NodePort https://github.com/fission/fission/releases/download/0.7.2/fission-all-0.7.2.tgz
```


---

If in a few days you find yourself setting up a cluster in Japan or Germany on [Linode], and another two in Australia and France on [vultr], then you may have just joined the PHC (Performance [Hobby Cluster]s) club. Some people tinker late at night on their truck, we benchmark and test the resilience of node failures on our overseas, budget kubernetes clusters. It's all about going big, on the cheap.

[![k8s performance hobby clusters](https://github.com/cjimti/mk/raw/master/images/content/k8s-tshirt-banner.jpg)](https://amzn.to/2wzP4mg)

[serverless]: https://en.wikipedia.org/wiki/Serverless_computing
[Vendor neutral]: https://searchitchannel.techtarget.com/definition/vendor-neutral
[vendor lock-in]: https://en.wikipedia.org/wiki/Vendor_lock-in
[AWS Lambda]: https://aws.amazon.com/lambda/
[Name Weasel]: https://amzn.to/2rTEaD0
[FaaS]: https://en.wikipedia.org/wiki/Function_as_a_service
[Amazon Echo]: https://amzn.to/2rUjPwJ
[OpenFaaS]: https://github.com/openfaas/faas
[OpenWhisk]: https://openwhisk.apache.org/
[Fission]: https://fission.io/
[kubeless]: https://github.com/kubeless/kubeless
[funktion]: https://github.com/funktionio/funktion
[Fission framework news]: https://www.infoworld.com/article/3157365/application-development/new-framework-uses-kubernetes-to-deliver-serverless-app-architecture.html

[common name]: https://www.quora.com/What-does-the-CN-name-in-a-client-certificate-refer-to
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
[Certificate]: https://cert-manager.readthedocs.io/en/latest/reference/certificates.html
[Secret]: https://kubernetes.io/docs/concepts/configuration/secret/
[Ingress on Custom Kubernetes]: https://mk.imti.co/web-cluster-ingress/
[NodePort]: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
[Service]: https://kubernetes.io/docs/concepts/services-networking/service/
[Go]: https://golang.org/
[Python3]: https://www.python.org/