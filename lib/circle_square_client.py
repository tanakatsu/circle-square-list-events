import requests
import re
import datetime
from bs4 import BeautifulSoup


class CircleSquareClient:
    LOGIN_URL = "https://www.c-sqr.net/login"
    LIST_URL = "https://www.c-sqr.net/events/list"

    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.client = requests.session()

    def get_event_list(self, target_date=None):  # targe_date: YYYY-MM-DD
        if target_date:
            if not re.match(r'\d\d\d\d-\d{1,2}-\d{1,2}', target_date):
                raise ValueError(f"invalid target_date: {target_date}")
            year = int(target_date.split("-")[0])
        else:
            year = datetime.date.today().year

        token = self._get_token(target_date)
        html = self._get_schedule_html(token)
        events = self._parse_html(html, year)
        return events

    def _get_token(self, target_date=None):
        list_url = CircleSquareClient.LIST_URL
        if target_date:
            list_url = f"{list_url}?date={target_date}"
        res = self.client.get(list_url)
        # print(res.status_code)
        matched = re.findall('<input type="hidden" name="_token" value="([^\"]+)"', res.text)
        token = matched[0]
        return token

    def _get_schedule_html(self, token):
        payload = {"account": self.account, "password": self.password, "_token": token}
        res = self.client.post(CircleSquareClient.LOGIN_URL, data=payload)
        # print(res.status_code)
        return res.text

    def _parse_html(self, html, year):
        soup = BeautifulSoup(html, "html.parser")

        elms = soup.select("#app > div.page-contents > div > div.page-main-full > main > div > ul > li > div > a > div.c-list-box__title")
        events = []
        for elm in elms:
            event_name = elm.text.strip().replace("\u3000", " ") 
            event_url = elm.parent.parent.select("a")[0].get("href")
            # print(event_name, event_url)
            sub_elms = elm.parent.select("li")
            dateinfo = sub_elms[2].text.lstrip("\n\xa0").strip()
            # print(dateinfo)
            m = re.match(r'(\d+\/\d+)\(.\)(\d+:\d+) - (\d+:\d+)', dateinfo)
            if m:
                start_time = f"{year}/{m.group(1)} {m.group(2)}"
                end_time = f"{year}/{m.group(1)} {m.group(3)}"
                # print(start_time, end_time)
            else:
                m2 = re.match(r'(\d+\/\d+)', dateinfo)
                start_time = f"{year}/{m2.group(1)}"
                end_time = f"{year}/{m2.group(1)}"
            events.append({"name": event_name,
                           "start_time": start_time,
                           "end_time": end_time,
                           "url": event_url,
                           })

        # print(events)
        return events
