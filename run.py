from scraper import BurgeramtScraper
from bot import BurgeramtBot

from log import setup_logging

import config


def main():
    setup_logging(debug=config.DEBUG, logging_level=config.LOGGING_LEVEL)
    scraper = BurgeramtScraper(
        base_url=config.SCRAPER_BASE_URL,
        uid=config.SCRAPER_UID,
        search_mode=config.SCRAPER_SEARCH_MODE,
    )
    bot = BurgeramtBot(token=config.TELEGRAM_API_TOKEN, scraper=scraper)
    bot.run()


if __name__ == "__main__":
    main()
