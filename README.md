### run


```depends
- redis
- mysql
```

```bash
$ pip install -r requirements.txt
$ python app.py

$ celery -A queue.enqueue worker --loglevel=info --autoscale=10,2 -n worker1.%h
```
