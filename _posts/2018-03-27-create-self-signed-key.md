---
published: false
title: Self-Signed SSL Certificate for Nginx Ingress
layout: post
tags: container-as-command emacs docker
---

The following helps generate a key pair, great for testing ingress controllers on [kubernetes] with Minikube.


```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout nginx-selfsigned.key \
     -out nginx-selfsigned.crt

openssl dhparam -out dhparam.pem 2048
```

Add keys as secrets to the cluster:
```bash
kubectl create secret tls tls-certificate \
     --key nginx-selfsigned.key \
     --cert nginx-selfsigned.crt

kubectl create secret generic tls-dhparam --from-file=dhparam.pem
```


