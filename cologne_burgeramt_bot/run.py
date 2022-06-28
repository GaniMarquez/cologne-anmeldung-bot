from cologne_burgeramt_bot.scraper import BurgeramtScraper
from cologne_burgeramt_bot.bot import BurgeramtBot
from cologne_burgeramt_bot.logger import setup_logging
from cologne_burgeramt_bot import config


def main():
    setup_logging(debug=config.DEBUG, logging_level=config.LOGGING_LEVEL)
    scraper = BurgeramtScraper(
        base_url=config.SCRAPER_BASE_URL,
        uid=config.SCRAPER_UID,
        search_mode=config.SCRAPER_SEARCH_MODE,
    )
    bot = BurgeramtBot(
        token=config.TELEGRAM_API_TOKEN,
        host=config.HOST,
        port=config.PORT,
        heroku_app=config.HEROUKU_APP,
        scraper=scraper,
    )
    bot.run()


if __name__ == "__main__":
    main()
