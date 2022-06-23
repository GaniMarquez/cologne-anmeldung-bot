from telegram.utils.helpers import escape_markdown
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from loguru import logger

import telegram

from anmeldung import AnmeldungScraper
from log import setup_logging

import config


def start_callback(update: Update, context: CallbackContext):
    info = {"chat_id": update.effective_chat.id}
    with logger.contextualize(info=info):
        logger.info("The start command has been triggered.")
        # context.bot.send_message(
        #     chat_id=update.effective_chat.id,
        #     text="Hi! Use `/check` to check for available schedules!",
        #     parse_mode=telegram.ParseMode.MARKDOWN,
        # )
        update.message.reply_text("Hi! \n Use /check to check for available schedules.")


def check_timeslots_callback(update: Update, context: CallbackContext):
    info = {"chat_id": update.effective_chat.id}
    with logger.contextualize(info=info):
        logger.debug("Started Scraper")
        scraper = AnmeldungScraper()
        schedules_df = scraper.run()
        logger.debug("Finished Scraper")
        schedules = []
        for _, row in schedules_df.iterrows():
            burgeramt_str = escape_markdown(f"{row.burgeramt}", version=2)
            available_date_str = escape_markdown(f"{row.available_date}", version=2)
            schedules.append(
                f"There are slots in *{burgeramt_str}* on *{available_date_str}* and the earliest available is at *{row.available_time}*\.\n"
            )
        import pdb

        pdb.set_trace()
        schedules.append(
            "Book your slots [here](https://termine.stadt-koeln.de/m/kundenzentren/extern/calendar/?uid=b5a5a394-ec33-4130-9af3-490f99517071&lang=de)\.",
        )
        schedules_str = "\n".join(schedules)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=schedules_str,
            parse_mode=telegram.ParseMode.MARKDOWN_V2,
        )


# def echo(update: Update, context: CallbackContext):
#     info = {"chat_id": update.effective_chat.id}
#     with logger.contextualize(info=info):
#         logger.info("Echoing all inputs fromt he user.")
#         response = "<pre>Available Amneldung Schedules:\n| Name | Age |\n|------|-----|\n| Gani | 27  |\n| Onik | 26  |\n</pre>"
#         context.bot.send_message(
#             chat_id=update.effective_chat.id, text=response, parse_mode=telegram.ParseMode.HTML
#         )


# def caps(update: Update, context: CallbackContext):
#     info = {"chat_id": update.effective_chat.id}
#     with logger.contextualize(info=info):
#         logger.info("caps command")
#         text_caps = " ".join(context.args).upper()
#         context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def main():
    setup_logging()

    updater = Updater(token=config.TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # start_handler = CommandHandler("start", start)
    # dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # caps_handler = CommandHandler("caps", caps)
    # dispatcher.add_handler(caps_handler)

    # Add different handlers to the Bot
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler("help", start_callback))
    dispatcher.add_handler(CommandHandler("check", check_timeslots_callback))
    # dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
