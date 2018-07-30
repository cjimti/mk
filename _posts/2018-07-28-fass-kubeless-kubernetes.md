---
published: false
layout: post
title: Kubernetes FaaS - Kubeless Python and Elasticsearch
tags: kubernetes elastic database
featured: elastic kubernetes python
mast: balloon
---

FaaS or [Function as a Service] also known as [Serverless computing] is often discussed in terms of cost savings or its relationship to the physical and network architecture of a platform. While many of the [cost and infrastructure] advantages of FaaS are compelling its only one of many advantages. Below, I hope to demonstrate how easy it is to develop and deploy FaaS components into a custom Kubernetes cluster. The functions I develop are nearly all business logic.

**Quick Reference:**

* Do not remove this line (for toc on a rendered blog)
{:toc}

## Architecture

Lately, I have been seeing a trend of comparisons between developing platforms with Monoliths, , and Functions as . I believe this comparison is flawed unless you are on a desert island and can only choose one implementation in which to develop your application. Even if you did have to limit your architecture to one concept, you would first need to have decided on a definitive standard in which you have delineated where a bloated microservice is really monolith, or a prewarmed FaaS is really just a microservice. If you are following my point, they can all have a place and definition is often relies on context. All these concepts can work together wonderfully, by operating in containers, orchestrated by Kubernetes.

![](/images/content/faas_architecture.png)

## Terminology

In this article I will use the term **Function** to describe a [Kubeless Function]. [Kubeless] is an implementation of FaaS [Function as a Service] also known as [Serverless computing], [Serverless], [lambda][AWS lambda], [Google functions] or even [Nano Services].

## Motivation

While our industry sorts out the distinctive and vocabulary of these new architectures, please bear with me while I show you a simplified example from, demonstrating an implementation I find successful. There are exciting and innovative ways that FaaS services can be triggered through a number of mechanisms, like Amazon's Alexa and it's use of lambda, however for simplicity I focus on the familiar needs of an HTTP API stack.

At this point most of my legacy systems are Monoliths, however they are containerized and live in the cluster as they would any hosting environment. Most of my Microservices are developed for generic or reusable functionality, and some are developed for more complex business logic. However, allowing data and actions to be pipelined between monoliths, microservices and functions, is a type of chaining gives me the **ability to use a Function as a means to inject business logic at any point in the platform without significant architectural changes.**


## Kubeless for FaaS

I really appreciate the simplicity and elegance of [Kubeless] and its seamless integration into Kubernetes. [Kubeless] is really an extension of the Kubernetes API and takes advantage of its stability and architecture. This integration with Kubernetes makes [Kubeless] incredibly easy if you are already familiar with Kubernetes.

[Kubeless] comes with its own CLI for interacting with Functions, providing command such as:

 ```bash
 kubeless function ls -n the-project

NAME        NAMESPACE      HANDLER           RUNTIME      DEPENDENCIES                STATUS
wx-stats    the-project    wx-stats.stats    python3.6    certifi==2018.4.16          1/1 READY
                                                          chardet==3.0.4
                                                          elasticsearch==6.3.0
                                                          elasticsearch-dsl==6.2.1
                                                          idna==2.7
                                                          ipaddress==1.0.22
                                                          python-dateutil==2.7.3
                                                          requests==2.19.1
                                                          six==1.11.0
                                                          urllib3==1.23
```

 However due to  [Kubeless] deep integration with Kubernetes, I often find myself executing kubectl commands simply out of habit:

```bash
kubectl get functions
```

This works because Kubless Function are merely Kubernetes objects, or Custom Resources to be accurate and many operations on them are as they would be with other resources in the cluster, like services, deployment or pods.

### Install Kubeless

[Kubeless] installs in the `kubeless` namespace by default and can be used to create functions in any namespace. I use [RBAC] for all my clusters and if you are looking to set up a custom Kubernetes cluster I recommend spending about an hour following my article [Production Hobby Cluster].

Setup is easy and the [official installation instructions] are clear.

### Toolchain and Local Development

Developing [Kubeless] Functions can be performed with the same tools as any other services. I build my [Golang] and [Python] functions with the commercial [Jet Brains] IDEs [Goland] and [PyCharm] however free IDEs such as [Visual Studio Code] and [Atom] work great as well.

In this demo my Functions are API endpoints that query [Elasticsearch], check out my article [Remote Query Elasticsearch on Kubernetes] on how I port-forward Kubernetes [Services] for remote access.

## Python Function

In this demo I am creating a function that returns the last 24 hours of weather data for Los Angeles, specifically temperatures. The data is aggregated into buckets of two-degree Fahrenheit intervals for later use in histograms and further analysis.

The [Elasticsearch DSL] is great library for working with Elasticsearch in [Python]. Although most of my Microservices are written in [Golang], [Python] provides a tremendous number of mature and well-documented libraries for working with data.

### Script wx-stats.py

The following is the script `wx-stats.py` containing the `stats` function I configure for use by [Kubeless]. I go over the script in detail further down.

`wx-stats.py`:
```python
#!/usr/bin/env python3
"""
Wx Stats from Elasticsearch

Local testing:
    kubectl port-forward service/elasticsearch 9200:9200 -n the-project
    HOST=localhost:9200 python ./wx-stats.py
"""
__author__ = "Craig Johnston"
__version__ = "0.0.1"
__license__ = "MIT"

import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections

host = os.environ['HOST']
connections.create_connection(hosts=[host], timeout=20)
client = Elasticsearch()
s = Search(using=client)


def stats(event, context):
    """
        Return wx stats
        Uses the Python Elasticsearch DSL
        https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
    """
    global s

    res = s.from_dict({
        "size": 0,
        "aggs": {
            "temps": {
                "histogram": {
                    "field": "rxtxMsg.payload.currently.temperature",
                    "interval": 2
                }
            }
        },
        "query": {
            "range": {
                "@timestamp": {
                    "gt": "now-24h"
                }
            }
        }
    }).execute()

    return res.to_dict()


if __name__ == '__main__':
    """
    Mock event and context for development
    See: https://kubeless.io/docs/kubeless-functions/
    """
    event = {}
    context = {}
    
    # json is only needed for development and testing
    # not necessary to import for Kubeless function
    import json
    
    json_string = json.dumps(stats(event, context), indent=2)
    print(json_string)

```




[Elasticsearch DSL]:https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
[Services]:https://kubernetes.io/docs/concepts/services-networking/service/
[Remote Query Elasticsearch on Kubernetes]:https://mk.imti.co/remote-query-kubernetes-elasticsearch/
[Elasticsearch]:https://mk.imti.co/kubernetes-production-elasticsearch/
[Atom]:https://atom.io/
[Visual Studio Code]:https://code.visualstudio.com/
[PyCharm]:https://www.jetbrains.com/pycharm/
[Goland]:https://www.jetbrains.com/go/
[Jet Brains]:https://www.jetbrains.com/
[Python]:https://www.python.org/
[Golang]:https://golang.org/
[Production Hobby Cluster]:https://mk.imti.co/hobby-cluster/
[official installation instructions]:https://kubeless.io/docs/quick-start/
[Function as a Service]:https://en.wikipedia.org/wiki/Function_as_a_service
[Serverless computing]:https://en.wikipedia.org/wiki/Serverless_computing
[cost and infrastructure]:https://martinfowler.com/articles/serverless.html#ReducedOperationalCost
[AWS lambda]:https://aws.amazon.com/lambda/
[Google functions]:https://cloud.google.com/functions/
[kubeless]:https://kubeless.io/
[Nano Services]:https://www.infoq.com/news/2014/05/nano-services
[Kubeless Function]:https://kubeless.io/docs/quick-start/
[RBAC]:https://kubernetes.io/docs/reference/access-authn-authz/rbac/
[Serverless]:https://serverless.com/