## Circle Square List Events

### What's this ?
Fetch events list from [Circle Square](https://www.c-sqr.net/) web service.

### Deploy as API server

#### Local server

```
$ pip install -r requirements.txt
$ uvicorn server:app
```

#### Heroku

```
$ git push heroku master
```

### Sample usage

```
$ curl -X POST -H "Content-Type: application/json" -d '{"account":"YOUR_ACCOUNT","password":"YOUR_PASSWORD"}' 127.0.0.1:8000/events
```

You'll receive something like this.
```
[
  {"name":"イベント1","start_time":"2023/6/3 09:00","end_time":"2023/6/3 11:30","url":"https://www.c-sqr.net/events/xxx"},
  {"name":"イベント2","start_time":"2023/6/4 09:00","end_time":"2023/6/4 11:30","url":"https://www.c-sqr.net/events/yyy"}
]
```

You can specify a target date.
```
$ curl -X POST -H "Content-Type: application/json" -d '{"account":"YOUR_ACCOUNT","password":"YOUR_PASSWORD", "date":"2023-07-01"}' 127.0.0.1:8000/events
```

