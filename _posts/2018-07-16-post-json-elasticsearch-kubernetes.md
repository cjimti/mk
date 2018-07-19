---
published: true
layout: post
title: High Traffic JSON Data into Elasticsearch on Kubernetes
tags: kubernetes elastic database
featured: kubernetes elastic docker
mast: water
---

IOT devices, Point-of-Sale systems, application events or any client that sends data destined for indexing in Elasticsearch often need to send and forget, however, unless that data is of low value there needs to be assurance that arrives at its final destination. Back-pressure and database outages can pose a considerable threat to data integrity. Publish-subscribe message ques like Kafka are abundant add incredible flexibility to data pipelines but can also suffer from data loss and duplication.

**Quick Reference:**

* Do not remove this line (for toc on a rendered blog)
{:toc}


## Background

What always kept me up at night is, what happens when Elasicsearh slows down, and back pressure remains to constant for indexing to catch up? In many of my systems, I needed an additional layer and in some systems where message queues like Kafka are overkill or not necessary I needed a failsafe. In the process below I demonstrate how I use [rxtx] to store and forward data to [rtBeat] which publishes it into Elasticsearch.

The process of store-and-forward can work without message queues or even complement them as an additional, early layer of buffering.

## Overview

Over the years I have made conscious efforts to move complexity further from the edge in server-side applications, even if this means an added layer of API/data management. An early layer of simplicity not only buffers API calls and data but moves complexity back a rung.



Using [rxtx] with [rtBeat] you can achieve high performance, highly available service for accepting JSON POST data and delivering it to Elasticsearch. [rxtx] collects post data, writes it to a local [bbolt] database and sends batches on an interval to rtBeat. [rtBeat] processes the batches of POSTed JSON data and publishes them as events into Elasticsearch. [rtBeat] is an Elastic [beat] and can publish simultaneously to [elasticsearch], [logstash], [kafka] and [redis].

## Store-and-forward - [rxtx]

[![](https://github.com/txn2/rxtx/raw/master/mast.jpg)][rxtx]

## Collect, buffer and publish - [rtBeat]

[![](https://raw.githubusercontent.com/txn2/rtbeat/master/mast-logo.jpg)][rtBeat]

## Test

## Bonus - Kubernetes Cron

## Conclusion

## Refrence
- [rtBeat] Docker container
- [rxtx] Docker container
- [Elasticsearch]
- Elastic [beat]

[bbolt]:https://github.com/coreos/bbolt
[beat]:https://www.elastic.co/products/beats
[elasticsearch]: https://www.elastic.co/
[logstash]: https://www.elastic.co/products/logstash
[kafka]: https://kafka.apache.org/
[redis]: https://redis.io/
[rtBeat]:https://hub.docker.com/r/txn2/rtbeat/
[rxtx]: https://hub.docker.com/r/txn2/rxtx/