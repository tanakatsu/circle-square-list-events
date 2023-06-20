from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, validator
import re
from circle_square_client import CircleSquareClient


class RequestEvents(BaseModel):
    account: str
    password: str
    date: Union[str, None]

    @validator('date')
    def check_format(cls, v, values, **kwargs):
        if v and not re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', v):
            raise ValueError('Must be YYYY-MM-DD.')
        return v

app = FastAPI()

@app.get("/hello")
def hello():
    return {"Hello": "World!"}


@app.post("/events")
def events(req_events: RequestEvents):
    account = req_events.account
    password = req_events.password
    date = req_events.date
    # print(account, password, date)
    client = CircleSquareClient(account, password)
    events = client.get_event_list(date)
    return events
