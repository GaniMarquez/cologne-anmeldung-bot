import pytz
import datetime as dtm

from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters, Defaults

import config


def job(context):
    chat_id = context.job.context
    local_now = dtm.datetime.now(context.bot.defaults.tzinfo)
    utc_now = dtm.datetime.utcnow()
    text = "Running job at {} in timezone {}, which equals {} UTC.".format(
        local_now, context.bot.defaults.tzinfo, utc_now
    )
    context.bot.send_message(chat_id=chat_id, text=text)


def echo(update, context):
    # Send with default parse mode
    update.message.reply_text("<b>{}</b>".format(update.message.text))
    # Override default parse mode locally
    update.message.reply_text("*{}*".format(update.message.text), parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*{}*".format(update.message.text), parse_mode=None)

    # Schedule job
    context.job_queue.run_once(
        job, dtm.datetime.now() + dtm.timedelta(seconds=1), context=update.effective_chat.id
    )


def main():
    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone("Europe/Berlin"))

    """Start the bot."""
    updater = Updater(config.TELEGRAM_API_TOKEN, use_context=True, defaults=defaults)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on non command text message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
