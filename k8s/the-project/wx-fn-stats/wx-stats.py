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

    print(context)

    return res.to_dict()


if __name__ == '__main__':
    """
    Mock event and context
    See: https://kubeless.io/docs/kubeless-functions/
    """
    import json
    event = {
        "data": "",
        "event-id": "test",
        "event-type": "application/json",
        "event-time": "",
        "event-namespace": "wx-stats.mk.imti.co",
        "extensions": {
            "request": {},
            "response": {}
        }
    }

    context = {
        "function-name": "mock",
        "timeout": "180",
        "runtime": "nodejs6",
        "memory-limit": "128M"
    }

    json_string = json.dumps(stats(event, context), indent=2)
    print(json_string)
