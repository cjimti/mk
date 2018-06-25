---
published: true
layout: post
title: A Microservices Workflow with Golang and Gitlab CI
tags: golang docker gitlab kubernetes
featured: golang docker gitlab kubernetes
mast: ci
---

Many of the resources on Cloud Native [Microservices] show you how easy it is to get up and running with AWS or GKE. I think this is great but for the fact that I see a trend (in my clients at least) of associating concepts with particular products or worse, companies (I love Amazon, but it's not THE cloud). In my opinion, to embrace Cloud Native and [Microservices], you should develop some, and host them yourself. The cloud is not Google or Amazon; it's any cluster of virtualized systems, abstracted from their hardware interfaces and centrally managed.

* Do not remove this line (for toc on a rendered blog)
{:toc}

## Overview

Alot of tutorials I run across assume you might get to live in a utopian world, where all your code is open source and hosted on public Github repositories and deployment means up and running a single node k8s cluster like Minikube. To be fair, this simplifies the technical details of the examples, and it broadens the audience by giving local sandbox examples that you can adapt to your production environment,  and helps many of us quickly get our head around novel concepts.

If you are like me your early days were developing Java or Perl scripts that were installed on dev, staging or production hardware and executed under the Apache or Tomcat web servers, and that may still be part of your architecture today. Big monolithic applications, running on big fast servers that you could visit at the data center. However many developers like myself have started moving new development to Cloud Native [Microservices].


## A Microservice Stack

I choose five technologies in my workflow to give you some examples. I am referring to open source (and free) software only, not services.

- **Kubernetes with Alpine Linux Docker** containers is the core of my cloud. This cloud can be run almost anywhere from AWS to [Vultr], [Digital Ocean], [Linode] or some co-located servers you have running in a data center. If you want to learn how to set up a production style Kubernetes cluster on the cheap, I suggest reading my post, [Production Hobby Cluster]. [Production Hobby Cluster] gets you a legit, highly available, three node Kuberneteds cluster for about $15 a month. Don't plan on hosting Netflix on it, but when you need to scale your architecture will not need a complete overhaul. Larger instances and more of them with scale the [Production Hobby Cluster] from hobby to enterprise.

- **Golang** / Go to write your [Microservices], those small API endpoints that satisfy some simple, single or small group of requirements. I use Go because it compiles to a self-sufficient little binary that runs at home in the [smallest of Docker containers][Building Docker Images for Static Go Binaries] and able to efficiently serve raw TCP or HTTP traffic on a specified port. Go is also an excellent language for [extending the cloud itself][Extending Kubernetes: Create Controllers for Core and Custom Resources] but that is a bit much for this article.

- **Gitlab** is my choice for self-hosted code and CI/CD (Automation). Github is fantastic and any code I do not need to keep private goes straight there; however even my open source projects get cloned into Gitlab so I can take advantage of its simple build and deployment automation. I run [Gitlab itself in my cloud][Installing GitLab on Kubernetes]. Some of my older projects run through Jenkins, and it's an excellent tool but overkill these days for most of our workflow, now that Gitlab has matured. Rather than pay for services I would rather pay for instnaces to grow my cluster and host more of my own services.


## The Microservice Application

The following is a simplified workflow.

An application and one or more libraries as separate repositories. Not every lib needs its own. However, it's a good idea to separate any libraries that many projects share. Examples would be common structs or system-wide service implementations.

- **The Microservice application**: `/go/src/gitlab.example.com/proj/app`
- **A library**: `/go/src/gitlab.example.com/lib/example`

### Workflow & Boilerplate

Golang with Gitlab and Kubernetes, Microservice application, file structure boilerplate:

```bash
README.md
main.go
Dockerfile
./k8s/dev
    10-namespace.yml
    20-service.yml
    30-config.yml
    40-deployment.yml
    50-ingress.yml
    README.md
.gitlab-ci.yml
```

I'll start at the top of the list of work down. Every repository needs a **README.md** with simple instruction for development and deployment, environment variables and build considerations. I opt for brief and straightforward documentation; I want my documentation as maintainable as my code. [Microservices] should have micro-documentation, everything you need and not more.

##### Source: `main.go` (`server.go`)

Most of my [Microservices] development start with something similar to this [server.go](https://github.com/txn2/boilerplate-go/blob/master/server.go) boilerplate, using fast and simple [gin-gonic](https://gin-gonic.github.io/gin/) for web/api framework and Uber's [zap](https://github.com/uber-go/zap) for "Blazing fast, structured, leveled logging".

What you don't see in the boilerplate are a few private libs that get added in depending on the project or specific service. These system-wide libs share business log and import from the private Gitlab repository.

```golang
import (
    "private-gitlab.example.com/some/lib"
    "private-gitlab.example.com/some/otherlib"
)
```

It can be tricky allowing external build systems to pull these private libraries; however that is overcome easily with Gitlab tokens and some updates to the `Dockerfile` and `.gitlab-ci.yml`.

##### Container: `Dockerfile`

Nearly all my [Microservices] use the same `Dockerfile`, there are some adjustments and variations, but most of the time this boilerplate gives me exactly what I need, a compiled binary in a super small Alpine Linux container.

```dockerfile
FROM golang:1.10.2-alpine3.7 AS builder

ARG GITLAB_TOKEN
ARG GITLAB_DOMAIN

RUN apk update \
 && apk add git

RUN mkdir -p /go/src \
 && mkdir -p /go/bin \
 && mkdir -p /go/pkg

ENV GOPATH=/go
ENV PATH=$GOPATH/bin:$PATH

RUN mkdir -p $GOPATH/src/app
ADD . $GOPATH/src/app

ADD . /go/src

WORKDIR $GOPATH/src/app

# go get uses git to pull lib dependencies
RUN git config --global url."https://oauth2:$GITLAB_TOKEN@$GITLAB_DOMAIN".insteadOf "https://$GITLAB_DOMAIN"

RUN go get .
RUN go get github.com/json-iterator/go
RUN CGO_ENABLED=0 go build -tags=jsoniter -a -installsuffix cgo -o /go/bin/server .

FROM alpine:3.7

WORKDIR /

COPY --from=builder /go/bin/server /server
ENTRYPOINT ["/server"]
```

**Grab a copy with wget if you like:**
```bash
wget https://gist.githubusercontent.com/cjimti/c988db3ff1a798eb3e18d76f3d71e75a/raw/adfaadc34c643f1af2c6ddfdc91aba80d6322fb7/Dockerfile
```

If your service needs to communicate out over https, you need to add `RUN apk add --no-cache ca-certificates` to install root certificates. However, I like to keep my containers as small as possible 5-15 megabyte range, so I only add what I need for the service. I could get these even smaller using [`scratch`][Building Docker Images for Static Go Binaries], but I find **Alpine Linux** a good balance.

An important feature of this Dockerfile is allowing `go` to `go get` libraries from the private Gitlab repository.  The two `ARG` lines, `GITLAB_TOKEN` and `GITLAB_DOMAIN` are populated in [docker build] command found `.gitlab-ci.yml` that I go over further down this article. The git configuration directive `RUN git config --global url."https://oauth2:$GITLAB_TOKEN@$GITLAB_DOMAIN".insteadOf "https://$GITLAB_DOMAIN"` tells git to prepend `oauth2:$GITLAB_TOKEN` when pulling from `$GITLAB_DOMAIN`. Since our `$GITLAB_DOMAIN` is a private repository we need to use a token to authenticate from within the Docker container during the build process.

I generate a Gilab token from a generic user that has access to all the repositories containing my privately shared libraries.

To test this container locally, you can run the [docker build] command found in `.gitlab-ci.yml` below.

```bash
docker build --build-arg GITLAB_TOKEN=$GITLAB_TOKEN \
--build-arg GITLAB_DOMAIN=$GITLAB_DOMAIN \
-t example_app .
```

First, you need to obtain a token from Gitlab, see below.

##### Gitlab User Token

You need to create a Gitlab user with access to specific repositories, groups, or all (or use your personal account if you work solo). If your team is small, you may not need fine-grained security here. Remember we only need read-only access, so it's not essential to keep the secret safe from anyone who already had read access. Make sure to copy the generated token to your notes for use further down to configure the Gitlab project.

![Gitlab Access Tokens](/images/content/gitlab_access_tokens.png)

All you need is the generated token, the **Name** is used for keeping track of your tokens in **Gitlab**.

#### Gitlab Project Settings: Secret Variables

Assuming you have already setup a Gitlab repository for your Microservice, add the **Secret variables** `GITLAB_DOMAIN` (should be something like gitlab.example.com,) review its use in the `Dockerfile` above, and GITLAB_TOKEN, the one we just generated. GITLAB_TOKEN allows `go get` to pull private libraries in from your imports.

There are ways to avoid having to `go get` dependencies, by using utilities like `godeps` and pre-packaging required libraries you don't have to retrieve them at build time. However, this can also make development difficult if you are actively developing those libraries at the same time, as I often do. The configuration above gives you the option to do it either way.

![Gitlab Project Settings](/images/content/gitlab_ci_cd_settings.png)

#### Kubernetes: `./k8s/dev`

My workflow starts with deploying a minimally working version of my microservice to a development environment; this can be a separate cluster, a just a separate [namespace]. I use a separate cluster. Setting up a cheap development cluster is easy and give your more opportunities to experiment, check out [Production Hobby Cluster] for an agile environment perfect for development and experimentation.

We use [kubectl] to configure and deploy the new service. I'll assume you have some familiarity with it. [kubectl] makes it easy to switch between multiple clusters: `kubectl config use-context phc-dev`, see my post, [kubectl Context Multiple Clusters](https://mk.imti.co/kubectl-remote-context/) for a detailed example.

##### Namespace: `./k8s/dev/10-namespace.yml`

I use a pretty standard form for all my Kubernetes objects. This example assumes we have a project called `the-project` and consists of many [Microservices]. Although the namespace is at the project level and not specific to a service, I keep a copy in each service. Duplicating this namespace configuration helps document the service and Kubernetes does not add the namespace if it already exists.

I also label every configuration with a **client** and **env**, this aids in selection rules and adds additional clarity of purpose.

**./k8s/dev/10-namespace.yml**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: the-project
  labels:
    client: internel
    env: dev
```

##### Service: `./k8s/dev/20-service.yml`

[Services] are persistent in Kubernetes, while [Pods] come and go, [Services] stick around and attach themselves to any [Pods] that match their selection rules. I like to setup services first to help illustrate this decoupled nature.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: example-microservice
  namespace: the-project
  labels:
    app: example-microservice
    client: internel
    env: dev
spec:
  selector:
    app: example-microservice
  ports:
    - protocol: "TCP"
      port: 8080
      targetPort: 8080
  type: ClusterIP
```

Most of my services attach to [Pods] with the same name as the service. The **name:** of my kubernetes object and **app:** labels nearly always match. I never prefix or suffix the object type as I have seen in some tutorials, this makes [kubectl] commands cleaner. Here are some examples of selecting all objects associated with a Microservice:

```bash
kubectl get all -l app=example-microservice -n the-project
```

I use **ClusterIP** for **type:** because I don't need a publicly accessible IP address or port. I use [Ingress on Custom Kubernetes].

##### Config: `./k8s/dev/30-config.yml`

Configuration using **30-config.yml** is optional since many of my [Microservices] share the same configuration. However, the setup is the same.

**Example `./k8s/dev/30-config.yml`**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-microservice
  namespace: the-project
  labels:
    app: example-microservice
    client: internel
    env: dev
data:
  dev_config.yml: |
    something:
      important: true
    token:
      encKey: "somethingsecure"
      expHours: 24
    cassandra:
      cluster: ["lax1.cas.example.com","ny1.cas.example.com"]
      keyspace: dev_app
```

In the deployment configuration below we mount this [ConfigMap] into the file system of our [Pod]. Mounting a [ConfigMap] as files allow our service to test outside the cloud with plain configuration files easily.

##### Deployment: `./k8s/dev/40-deployment.yml`

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-microservice
  namespace: fuse
  labels:
    app: example-microservice
    client: jakes
    env: dev
spec:
  replicas: 2
  selector:
    matchLabels:
      app: example-microservice
  template:
    metadata:
      labels:
        app: example-microservice
        client: jakes
        env: dev
    spec:
      imagePullSecrets:
        - name: example-microservice-regcred # see k8s/README.md
      volumes:
        - name: config-volume
          configMap:
            # ConfigMap specified in 30-config.yml
            name: example-microservice
      containers:
        - name: api5-auth
          # subsequent releases will use gitlab dev-PIPELINE_ID
          image: private-registry.example.com:5050/the-project/example-microservice:dev-latest
          imagePullPolicy: Always
          volumeMounts:
          - name: config-volume
            mountPath: /configs
          env:
            - name: BASE_PATH
              value: "/example/api/endpoint"
            - name: CONFIG
              value: "/configs/dev_config.yml"
            - name: DEBUG
              value: "true"
            - name: PORT
              value: "8080"
            - name: AGENT
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
          ports:
            - name: tcp
              containerPort: 8080
```

Before running you need another token from Gitlab, a Deploy Token Kubernetes needs in order to pull the image from Gitlab's repository.

##### Gitlab Project Settings: Generate Gitlab Deploy Token

In Gitlab under the repository settings for your **example-microservice**, choose **Repository** and expand the **Deploy Tokens** section. Create a deploy token by giving it a name (I leave the expiration empty) and check the **read_registry** scope. You need the genereated **Username** and token below, keep them in your notes.

![Gitlab Deploy Token](/images/content/gitlab_deploy_token.png)

 In the `40-deployment.yml` file above you can review the entry under **imagePullSecrets** to see we refrence **example-microservice-regcred**.

Create the **example-microservice-regcred** [Secret] in Kubernetes:

```bash
kubectl create secret docker-registry example-microservice-regcred \
    --namespace=the-project \
    --docker-server=private-registry.example.com:5050 \
    --docker-username=gitlab+deploy-token-8 \
    --docker-password=GHKddKqY1gzW86yllh3x \
    --docker-email=developer@example.com
```

The `kubectl create secret` command create a special kind of [Secret], [docker-registry](https://kubernetes-v1-4.github.io/docs/user-guide/kubectl/kubectl_create_secret_docker-registry/) used by Kubernetes when issuing pulls for Docker containers. This secret is make available for all the [deployments] in the `the-project` [namespace]. The `--docker-server` parameter specifies the repositor host and port. In this case we use the [Gitlab container registry] of our private Gitlab installation. The `--docker-username` and `--docker-password` parameters were generated above.

Once the secret is created it can be used by adding `example-microservice-regcred` in the **imagePullSecrets** for our **example-microservice** [deployment].

##### Ingress `./k8s/dev/50-ingress.yml`

Setup [Ingress on Custom Kubernetes] if you have not done so already. You should also secure your [ingress] api enpoints with HTTPS, a secure, free and easy way of doing this involves setting up [Let's Encrypt on Kubernetes] with [cert-manager](https://github.com/jetstack/cert-manager/).

**50-ingress.yml**

The following [Ingress on Custom Kubernetes] configuration directs traffic for **HTTP port 80** and **HTTPS port 443** on our example domain **api.the-project.dev.example.com** to port 8080 on the **example-microservice** we setup in [Services] configuration [`20-service.yml` above](#service-k8sdev20-serviceyml).

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: example-microservice
  namespace: the-project
  labels:
    app: example-microservice
    client: internel
    env: dev
spec:
  rules:
  - host: api.the-project.dev.example.com
    http:
      paths:
      - backend:
          serviceName: example-microservice
          servicePort: 8080
        path: /example/api/endpoint
  tls:
  - hosts:
    - api.example.com
    secretName: the-project-dev-production-tls
```

#### Initial Kubernetes Deployment

I never automate the initial configuration and deployment of [Microservices] in Kubernetes. There are a few things that once setup don't need to change per itteration. Packing the the install for automaic configuration and deployment is better left the the Kubernetes package manager [Helm] and after development itterations have stabelized into a more mature state, in this example workflow we are just getting started.

**The quick way**:

```bash
cd ./k8s/dev

kubectl create -f .
```

**The sane way**:

```bash
cd ./k8s/dev

kubectl create -f ./10-namespace.yml
kubectl create -f ./20-service.yml
kubectl create -f ./30-config.yml
kubectl create -f ./40-deployment.yml
kubectl create -f ./50-ingress.yml
```

You should now have a couple of [Pods], a [Deployment], a [ConfigMap], a [Service] and [Ingress] all labeled with `app: example-microservice` in the [namespace] `the-project`.

List the Kubernetes objects:

```bash
kubectl get po,svc,deploy,ing -l app=example-microservice -n the-project
```

#### Automated Builds and Deployments: `.gitlab-ci.yml`

## Resources
- [Production Hobby Cluster]
- [Ingress on Custom Kubernetes]
- [Let's Encrypt on Kubernetes]
- [Extending Kubernetes: Create Controllers for Core and Custom Resources]
- The package manger [Helm on Custom Kubernetes]

[Building Docker Images for Static Go Binaries]:https://medium.com/@kelseyhightower/optimizing-docker-images-for-static-binaries-b5696e26eb07
[Production Hobby Cluster]: https://mk.imti.co/hobby-cluster/
[Digital Ocean]: https://m.do.co/c/97b733e7eba4
[Vultr]: https://www.vultr.com/?ref=7418713
[Linode]: https://www.linode.com/?r=848a6b0b21dc8edd33124f05ec8f99207ccddfde
[Extending Kubernetes: Create Controllers for Core and Custom Resources]: https://medium.com/@trstringer/create-kubernetes-controllers-for-core-and-custom-resources-62fc35ad64a3
[Installing GitLab on Kubernetes]: https://docs.gitlab.com/ee/install/kubernetes/index.html
[Docker build]:https://docs.docker.com/engine/reference/commandline/build/
[namespace]:https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
[kubectl]:https://kubernetes.io/docs/tasks/tools/install-kubectl/
[Pods]:https://kubernetes.io/docs/concepts/workloads/pods/pod/
[Pod]:https://kubernetes.io/docs/concepts/workloads/pods/pod/
[Services]:https://kubernetes.io/docs/concepts/services-networking/service/
[Ingress on Custom Kubernetes]:https://mk.imti.co/web-cluster-ingress/
[ConfigMap]:https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
[Secret]:https://kubernetes.io/docs/concepts/configuration/secret/
[deployments]:https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
[deployment]:https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
[Gitlab container registry]:https://docs.gitlab.com/ee/user/project/container_registry.html
[Let's Encrypt, Kubernetes]:https://mk.imti.co/lets-encrypt-kubernetes/
[Let's Encrypt on Kubernetes]:https://mk.imti.co/lets-encrypt-kubernetes/
[Microservices]:https://mk.imti.co/microservices/
[Ingress on Custom Kubernetes]:https://mk.imti.co/web-cluster-ingress/
[Helm]:https://mk.imti.co/helm-on-custom-cluster/
[Helm on Custom Kubernetes]:https://mk.imti.co/helm-on-custom-cluster/