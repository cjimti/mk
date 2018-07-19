# Dark Sky API

Wx data for `the-project` uses the [Dark Sky API] which offers 1000 API calls per day for free.

The **wx-data** cron job sets an environment variable with an API key.

- Signup for a [Dark Sky API] developer account.
- Create a file called **apikey** with your secret API ky in it.

Create the Kubernetes secret:

```bash
kubectl create secret generic wd-data-api-key --from-file=apikey -n the-project
```

[Dark Sky API]:https://darksky.net/dev