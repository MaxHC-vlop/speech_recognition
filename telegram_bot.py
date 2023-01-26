import logging

from logs_handler import TelegramLogsHandler
from dialogflow_utils import detect_intent_texts

import telegram

from telegram import Update
from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters, CallbackContext
from telegram.ext import MessageHandler
from environs import Env


logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    message = f'Здравствуй, {username}'

    update.message.reply_text(message)


def send_dialogflow_message(update: Update, context: CallbackContext) -> None:
    session_id = update.message.from_user.id
    dialogflow_response, is_fallback = detect_intent_texts(
        context.bot_data['project_id'],
        session_id,
        [update.message.text], 'ru')

    update.message.reply_text(dialogflow_response)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(process)d %(levelname)s %(message)s"
    )

    env = Env()
    env.read_env()

    telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')
    logger_bot_token = env.str('LOGGER_BOT_TOKEN')
    chat_id = env.str('ADMIN_CHAT_ID')
    project_id = env.str('PROJECT_ID')

    logs = telegram.Bot(logger_bot_token)
    logger.addHandler(TelegramLogsHandler(logs, chat_id))
    logger.info('Start telegram bot.')

    updater = Updater(telegram_bot_token)

    dispatcher = updater.dispatcher
    dispatcher.bot_data = {'project_id': project_id}

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text, send_dialogflow_message)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
