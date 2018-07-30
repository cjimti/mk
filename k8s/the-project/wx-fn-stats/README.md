# Kubless Example


```bash
kubeless function update wx-stats --runtime python3.6 \
                                  --from-file wx-stats.py \
                                  --dependencies requirements.txt \
                                  --handler wx-stats.stats \
                                  --env HOST=elasticsearch:9200 \
                                  -n the-project
```
