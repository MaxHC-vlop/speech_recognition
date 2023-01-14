import logging
import os

from dialogflow_utils import detect_intent_texts

from telegram import Update
from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters, CallbackContext
from telegram.ext import MessageHandler
from environs import Env


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    message = f'Здравствуй, {username}'

    update.message.reply_text(message)


def send_dialogflow_message(update: Update, context: CallbackContext) -> None:
    session_id = update.message.from_user.id
    dialogflow_response, is_fallback = detect_intent_texts(
        os.getenv('PROJECT_ID'),
        session_id,
        [update.message.text], 'ru')

    update.message.reply_text(dialogflow_response)


def main() -> None:
    env = Env()
    env.read_env()

    telegram_token = env.str('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text, send_dialogflow_message)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
