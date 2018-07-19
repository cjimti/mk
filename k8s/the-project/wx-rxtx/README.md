## [Basic Auth]

Begin with using the [htpasswd] command to generate the file `auth` with a user named **wxrxtx** and a password specified when prompted. [kubectl] uses this file as-generated to create the appropriate [Secret] needed for Basic Auth.

```bash
htpasswd -c ./auth wxrxtx
```

In this example, I create a user named **kibop** for Basic Auth, kubectl pulls the user and password combination for **kibop** from the **auth** file created above and uses the filename as the key. It is essential to name the file **auth** since this is a necessary key for Ingress to find the Basic Auth credentials.

```bash
kubectl create secret generic wxrxtx-basic-auth --from-file auth -n the-project
```

Our namespace `the-project` now has the secret **wxrxtx-basic-auth** we use to password-protect wx-rxtx in the [ingress] configuration.

[Secret]:https://kubernetes.io/docs/concepts/configuration/secret/
[htpasswd]:https://httpd.apache.org/docs/2.4/programs/htpasswd.html
[kubectl]:https://kubernetes.io/docs/reference/kubectl/cheatsheet/
[Ingress]:https://mk.imti.co/web-cluster-ingress/
[Basic Auth]: https://mk.imti.co/kubernetes-ingress-basic-auth/
