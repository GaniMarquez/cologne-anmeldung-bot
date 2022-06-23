from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Union
from urllib.parse import urlparse
from urllib.parse import parse_qs

from bs4 import BeautifulSoup
from loguru import logger

import pandas as pd
import requests


@dataclass
class BurgeramtScraper(object):
    base_url: str
    uid: str
    search_mode: str
    search_timeslots_url: str = field(init=False)
    lang: str = "de"

    def __post_init__(self):
        self.search_timeslots_url = f"{self.base_url}/search_result"

    def get_online_reservation_landing_page(
        self, params: Dict, headers: Dict
    ) -> Union[requests.Response, Dict]:
        logger.debug("Sending request to the online reservation landing page.")
        response = requests.get(self.base_url, params=params, headers=headers, allow_redirects=True)
        query_string = self.parse_qs(response.url)
        return response, query_string

    def post_online_reservation_page(
        self, params: Dict, data: List[Tuple], headers: Dict
    ) -> Union[requests.Response, Dict]:
        logger.debug("Sending request to the online reservation page.")
        response = requests.post(self.base_url, params=params, headers=headers, data=data)
        query_string = self.parse_qs(response.url)
        return response, query_string

    def get_available_timeslots(self, params: Dict, headers: Dict) -> requests.Response:
        logger.debug("Sending request to the fetch the available timeslots.")
        response = requests.get(self.search_timeslots_url, params=params, headers=headers)
        return response

    def run(self) -> pd.DataFrame:
        params = self.generate_params(uid=self.uid, lang=self.lang)
        headers = self.generate_headers()
        response, qs = self.get_online_reservation_landing_page(params, headers)

        params = self.generate_params(uid=self.uid, wsid=qs["wsid"][0], lang=self.lang)
        data = self.generate_form_data()
        headers = self.generate_headers(cookie=response.request.headers["Cookie"])
        response, qs = self.post_online_reservation_page(params, data, headers)

        params = self.generate_params(
            uid=self.uid, wsid=qs["wsid"][0], search_mode=self.search_mode
        )
        headers = self.generate_headers(cookie=response.request.headers["Cookie"])
        response = self.get_available_timeslots(params, headers)

        schedules = self.parse_html(response)
        df = self.load_to_df(schedules)

        return df

    def generate_headers(self, cookie: str = None) -> Dict:
        headers = {
            "Accept-Language": "en",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }
        if cookie:
            headers.update({"Cookie": cookie})
        return headers

    def generate_form_data(self, count: int = 1) -> List[Tuple]:
        data = [
            ("action_type", ""),
            ("steps", "serviceslocationssearch_resultsbookingfinish"),
            ("step_current", "services"),
            ("step_current_index", "0"),
            ("step_goto", "+1"),
            ("services", ""),
            ("services", "e1d5bacf-1498-44c6-9489-2dbc7e322dec"),
            ("service_e1d5bacf-1498-44c6-9489-2dbc7e322dec_amount", ""),
            ("services", "44db93c7-379d-41b1-a06d-11820b1b71eb"),
            ("service_44db93c7-379d-41b1-a06d-11820b1b71eb_amount", ""),
            ("services", "d29a92ab-4112-40c5-b772-427ce186cc35"),
            ("service_d29a92ab-4112-40c5-b772-427ce186cc35_amount", ""),
            ("services", "d1c1e4d7-44a6-434d-884c-6aa1fe43d7a1"),
            ("service_d1c1e4d7-44a6-434d-884c-6aa1fe43d7a1_amount", ""),
            ("services", "58f5b5d5-4400-4d21-86bb-ae57bb6dc78a"),
            ("service_58f5b5d5-4400-4d21-86bb-ae57bb6dc78a_amount", ""),
            ("services", "0d2f4ea5-74f2-4699-b954-8907a1ca5f80"),
            ("service_0d2f4ea5-74f2-4699-b954-8907a1ca5f80_amount", f"{count}"),
            ("services", "d528518e-95c3-4dd8-850f-2db689fe0551"),
            ("service_d528518e-95c3-4dd8-850f-2db689fe0551_amount", ""),
            ("services", "2307dc91-2bca-4b30-a8ac-eb1a03b4b3a2"),
            ("service_2307dc91-2bca-4b30-a8ac-eb1a03b4b3a2_amount", ""),
            ("services", "b9028f0e-2b37-41c1-9176-966da3823e88"),
            ("service_b9028f0e-2b37-41c1-9176-966da3823e88_amount", ""),
            ("services", "24194702-ab60-4ea0-9c64-647797f5267b"),
            ("service_24194702-ab60-4ea0-9c64-647797f5267b_amount", ""),
            ("services", "638de2ae-20e3-4902-be70-aacd9e314fd1"),
            ("service_638de2ae-20e3-4902-be70-aacd9e314fd1_amount", ""),
            ("services", "179c690a-ef74-46c8-a6a3-d65269729601"),
            ("service_179c690a-ef74-46c8-a6a3-d65269729601_amount", ""),
            ("services", "e9e6d2eb-67ae-4e09-aa06-56b37d1b3467"),
            ("service_e9e6d2eb-67ae-4e09-aa06-56b37d1b3467_amount", ""),
            ("services", "057d9cf7-3d7b-4d40-a578-f4ed2e2432b2"),
            ("service_057d9cf7-3d7b-4d40-a578-f4ed2e2432b2_amount", ""),
            ("services", "631bf247-a668-48b0-9f05-015322f379bb"),
            ("service_631bf247-a668-48b0-9f05-015322f379bb_amount", ""),
        ]
        return data

    def generate_params(
        self, uid: str, wsid: str = None, lang: str = None, search_mode: str = None
    ) -> Dict:
        params = {"uid": uid}
        if wsid:
            params["wsid"] = wsid
        if lang:
            params["lang"] = lang
        if search_mode:
            params["search_mode"] = search_mode
        return params

    def parse_qs(self, url: str) -> Dict:
        parsed_url = urlparse(url)
        query_string = parse_qs(parsed_url.query)
        return query_string

    def parse_html(self, response: requests.Response) -> List:
        logger.debug("Parsing the fetched schedules from the online reservation system.")
        schedules = []
        soup = BeautifulSoup(response.text, "lxml")
        for div in soup.find_all("div", attrs={"class": "rc_appointment_possible"}):
            burgeramt = div.find("i", {"class": ["map", "marker"]}).parent.text
            burgeramt = burgeramt.split(": ", maxsplit=1)[-1]
            schedule = div.find("i", {"class": ["calendar"]}).parent.text
            date, time = schedule.split(" ", maxsplit=1)
            schedules.append(
                {"burgeramt": burgeramt, "available_date": date, "available_time": time}
            )
        return schedules

    def load_to_df(self, schedules: List) -> pd.DataFrame:
        logger.debug("Loading schdules to a dataframe for preprocessing.")
        df = pd.DataFrame.from_dict(schedules)
        df["available_date"] = pd.to_datetime(df["available_date"], dayfirst=True).dt.date
        df["available_time"] = pd.to_datetime(df["available_time"], format="%H:%M").dt.time
        return df.sort_values(by=["available_date", "available_time"])
