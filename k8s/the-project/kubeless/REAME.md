# Kubless Example


```bash
kubeless function deploy okfunc --runtime python3.6 \
                                --from-file ok-func.py \
                                --dependencies requirements.txt \
                                --handler ok-func.ok \
                                -n the-project
```