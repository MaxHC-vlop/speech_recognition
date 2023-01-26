import random
import logging

from logs_handler import TelegramLogsHandler
from dialogflow_utils import detect_intent_texts

import vk_api as vk
import telegram

from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


logger = logging.getLogger(__file__)


def send_dialogflow_message(event, vk_api, project_id):
    dialogflow_response, is_fallback = detect_intent_texts(
        project_id,
        event.user_id,
        [event.text], 'ru')

    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response,
            random_id=random.randint(1, 1000)
        )


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(process)d %(levelname)s %(message)s"
    )

    env = Env()
    env.read_env()

    vk_token = env.str('VK_BOT_TOKEN')
    logger_bot_token = env.str('LOGGER_BOT_TOKEN')
    chat_id = env.str('ADMIN_CHAT_ID')
    project_id = env.str('PROJECT_ID')

    logs = telegram.Bot(logger_bot_token)
    logger.addHandler(TelegramLogsHandler(logs, chat_id))
    logger.info('Start vk bot.')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_dialogflow_message(event, vk_api, project_id)


if __name__ == "__main__":
    main()
