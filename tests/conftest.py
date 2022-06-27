from dotenv import load_dotenv

import pytest


@pytest.fixture(scope="function")
def config():
    from cologne_burgeramt_bot import config

    return config


@pytest.fixture(scope="function")
def scraper(config):
    from cologne_burgeramt_bot.scraper import BurgeramtScraper

    scraper = BurgeramtScraper(
        base_url=config.SCRAPER_BASE_URL,
        uid=config.SCRAPER_UID,
        search_mode=config.SCRAPER_SEARCH_MODE,
    )

    return scraper


@pytest.fixture(scope="function")
def user_agent():
    from cologne_burgeramt_bot.user_agent import UserAgentRotator

    return UserAgentRotator().get_user_agent()


# @pytest.fixture(scope="function")
# def mock_(mocker):
#     s3 = mocker.MagicMock()
#     mocker.patch("boto3.client", return_value=s3)
#     return s3


@pytest.fixture(scope="session", autouse=True)
def session(session_mocker):
    # Start-Up
    session_mocker.patch("dotenv.load_dotenv", return_value=load_dotenv(".env.example"))

    # Test
    yield

    # Teardown
