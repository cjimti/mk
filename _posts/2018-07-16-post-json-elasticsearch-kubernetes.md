---
published: false
layout: post
title: POST JSON to Elasticsearch in Kubernetes
tags: kubernetes elastic database
featured: kubernetes elastic docker
mast: water
---

Using [rxtx] with [rtBeat] you can achieve a high performance, highly available service for accepting JSON POST data and delivering it to Elasticsearch. [rxtx] collects post data, writes it to a local [bbolt] database and sends batches on interval to rtBeat. [rtBeat] processes the batches of POSTed JSON data and publishes them as events into Elasticsearch. [rtBeat] is an Elastic [beat] and can publish simultainously to not only [elasticsearch] but [logstash], [kafka] and [redis] as well.

**Quick Reference:**

* Do not remove this line (for toc on a rendered blog)
{:toc}

[![](https://github.com/txn2/rxtx/raw/master/mast.jpg)][rxtx]
[![](https://raw.githubusercontent.com/txn2/rtbeat/master/mast-logo.jpg)][rtBeat]

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