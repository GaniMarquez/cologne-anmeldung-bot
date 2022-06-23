from dataclasses import dataclass, field

from telegram.utils.helpers import escape_markdown
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    Dispatcher,
)
from loguru import logger

import telegram

from scraper import BurgeramtScraper


@dataclass
class BurgeramtBot(object):
    token: str
    scraper: BurgeramtScraper
    updater: Updater = field(init=False)
    dispatcher: Dispatcher = field(init=False)

    def __post_init__(self):
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler("start", self.__start_callback))
        self.dispatcher.add_handler(CommandHandler("help", self.__start_callback))
        self.dispatcher.add_handler(CommandHandler("check", self.__check_callback))

    def __start_callback(self, update: Update, context: CallbackContext):
        info = {"chat_id": update.effective_chat.id}
        with logger.contextualize(info=info):
            logger.info("The start command has been triggered.")
            update.message.reply_text(
                "Welcome to the Burgeramt Bot for Cologne, Germany!\n\n"
                + "Use the follow commands for the Telegram Bot:\n"
                + "\t\t\t/check - check for available schedules\n"
                + "\t\t\t/help - check this menu again"
            )

    def __check_callback(self, update: Update, context: CallbackContext):
        info = {"chat_id": update.effective_chat.id}
        with logger.contextualize(info=info):
            logger.info("Started /check callback.")
            update.message.reply_text(
                "Hold on tight! Currently getting data from the Online Reservation System."
            )
            logger.info("Starting Burgeramt Scraper for Cologne, Germany.")
            schedules_df = self.scraper.run()
            logger.info(
                f"Finished Burgeramt Scraper for Cologne, Germany. A total of {schedules_df.shape[0]} Burgeramt Schedules scraped from the listings."
            )
            schedules = ["*Cologne Burgeramt Schedules*\n"]
            for _, row in schedules_df.iterrows():
                burgeramt_str = escape_markdown(f"{row.burgeramt}", version=2)
                available_date_str = escape_markdown(f"{row.available_date}", version=2)
                schedules.append(
                    f"There are slots in *{burgeramt_str}* on *{available_date_str}* and the earliest available is at *{row.available_time}*\.\n"
                )
                logger.debug(
                    f"Scraped Burgeramt Schedule. (Burgeramt: {row.burgeramt}, Date: {row.available_date}, Earliest Timeslot: {row.available_time})"
                )
            schedules.append(
                "Book your schedule for any of these timeslots [here](https://termine.stadt-koeln.de/m/kundenzentren/extern/calendar/?uid=b5a5a394-ec33-4130-9af3-490f99517071&lang=de)\.",
            )
            schedules_str = "\n".join(schedules)
            logger.info("Finished /check callback.")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=schedules_str,
                parse_mode=telegram.ParseMode.MARKDOWN_V2,
            )

    def run(self):
        self.updater.start_polling()
        # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
        # SIGABRT. This should be used most of the time, since start_polling() is
        # non-blocking and will stop the bot gracefully.
        self.updater.idle()
