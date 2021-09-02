
"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import yfinance as yf
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1957192471:AAH9usVw8M9j5-Wsm5Bh5PgWv_5dCkEisk4'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def getStock(update,context):
    ticker = update.message.text.strip().lower()
    # Retrieve Data from yafoo finance about the ticker
    data = yf.download(tickers = ticker, period='5m', interval='1m')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        update.message.reply_text('Close Price of {ticker} for past 5 minutes:'+'\n'+data['Close'].to_string(header=False))
    else:
        update.message.reply_text("No data found!")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text,getStock))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://cryptic-stream-96120.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

# Push to heroku:
# git add .
# git commit -m "first commit"
# heroku git:remote -a cryptic-stream-96120
# git push heroku master