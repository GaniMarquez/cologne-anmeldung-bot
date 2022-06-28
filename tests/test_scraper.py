import datetime

from requests import Response
from requests import codes

import pandas as pd


EXPECTED_STATUS_CODE = codes.ok
EXPECTED_QS = {
    "uid": ["b5a5a394-ec33-4130-9af3-490f99517071"],
    "wsid": ["2de3ad0f-4bed-4b46-8eca-7325e4c53585"],
    "lang": ["de"],
}
EXPECTED_DF = pd.DataFrame.from_dict(
    {
        "burgeramt": {
            0: "Temporäre Ausweis- und Meldestelle Kalk",
            1: "Kundenzentrum Rodenkirchen",
            2: "Kundenzentrum Kalk",
            3: "Kundenzentrum Chorweiler",
            4: "Kundenzentrum Innenstadt",
            5: "Kundenzentrum Mülheim",
            6: "Kundenzentrum Nippes",
            7: "Kundenzentrum Ehrenfeld",
            8: "Kundenzentrum Porz",
            9: "Kundenzentrum Lindenthal",
        },
        "available_date": {
            0: datetime.date(2022, 6, 27),
            1: datetime.date(2022, 6, 28),
            2: datetime.date(2022, 8, 19),
            3: datetime.date(2022, 8, 23),
            4: datetime.date(2022, 8, 23),
            5: datetime.date(2022, 8, 25),
            6: datetime.date(2022, 8, 25),
            7: datetime.date(2022, 8, 25),
            8: datetime.date(2022, 8, 25),
            9: datetime.date(2022, 8, 25),
        },
        "available_time": {
            0: datetime.time(10, 10),
            1: datetime.time(15, 10),
            2: datetime.time(10, 10),
            3: datetime.time(9, 40),
            4: datetime.time(11, 40),
            5: datetime.time(7, 30),
            6: datetime.time(7, 50),
            7: datetime.time(8, 10),
            8: datetime.time(11, 10),
            9: datetime.time(12, 10),
        },
    }
)

MOCK_RESPONSE_URL = "https://termine.stadt-koeln.de/m/kundenzentren/extern/calendar?uid=b5a5a394-ec33-4130-9af3-490f99517071&wsid=2de3ad0f-4bed-4b46-8eca-7325e4c53585&lang=de"
MOCK_COOKIE = "ASP.NET_SessionId=q0idobb0fuhnydysln42aqb2"


def test_get_online_reservation_landing_page(session_mocker, scraper, user_agent):
    mock_response = Response()
    mock_response.status_code = EXPECTED_STATUS_CODE
    mock_response.url = MOCK_RESPONSE_URL
    session_mocker.patch("requests.get", return_value=mock_response)

    params = scraper.generate_params(uid=scraper.uid, lang=scraper.lang)
    headers = scraper.generate_headers(user_agent=user_agent)
    response, qs = scraper.get_online_reservation_landing_page(params, headers)

    assert (
        EXPECTED_STATUS_CODE == response.status_code
    ), "Expected and received status code did not match."
    assert EXPECTED_QS == qs, "Expected and received query string did not match."


def test_post_online_reservation_page(session_mocker, scraper, user_agent):
    mock_response = Response()
    mock_response.status_code = EXPECTED_STATUS_CODE
    mock_response.url = MOCK_RESPONSE_URL
    session_mocker.patch("requests.post", return_value=mock_response)

    params = scraper.generate_params(
        uid=scraper.uid, wsid=EXPECTED_QS["wsid"][0], lang=scraper.lang
    )
    data = scraper.generate_form_data()
    headers = scraper.generate_headers(user_agent=user_agent, cookie=MOCK_COOKIE)
    response, qs = scraper.post_online_reservation_page(params, data, headers)

    assert (
        EXPECTED_STATUS_CODE == response.status_code
    ), "Expected and received status code did not match."
    assert EXPECTED_QS == qs, "Expected and received query string did not match."


def test_get_available_timeslots(session_mocker, scraper, user_agent):
    mock_response = Response()
    mock_response.status_code = EXPECTED_STATUS_CODE
    with open("tests/files/schedules.html", "rb") as f:
        mock_response._content = f.read()
    session_mocker.patch("requests.get", return_value=mock_response)

    params = scraper.generate_params(
        uid=scraper.uid,
        wsid=EXPECTED_QS["wsid"][0],
        lang=scraper.lang,
        search_mode=scraper.search_mode,
    )
    headers = scraper.generate_headers(user_agent=user_agent, cookie=MOCK_COOKIE)
    response = scraper.get_available_timeslots(params, headers)

    assert (
        EXPECTED_STATUS_CODE == response.status_code
    ), "Expected and received status code did not match."

    schedules = scraper.parse_html(response)
    df = scraper.load_to_df(schedules)

    assert EXPECTED_DF.equals(df), "Expected and extracted dataframe did not match."
