import random
import os

from dialogflow_utils import detect_intent_texts

import vk_api as vk

from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


def send_dialogflow_message(event, vk_api):
    dialogflow_response = detect_intent_texts(
        os.getenv('DIALOD_ID'),
        event.user_id,
        [event.text], 'ru')

    vk_api.messages.send(
        user_id=event.user_id,
        message=dialogflow_response,
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_dialogflow_message(event, vk_api)


if __name__ == "__main__":
    main()
