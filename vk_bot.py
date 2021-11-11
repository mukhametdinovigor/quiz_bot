import logging
import random

from environs import Env
import redis
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from quiz_questions import get_random_question
from tg_logs_handler import TelegramLogsHandler

logger = logging.getLogger('Logger')
env = Env()
env.read_env()


def create_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.SECONDARY)
    return keyboard


def handle_user_input(event, vk_api, keyboard, redis_db):
    right_answer = redis_db.get(f'vk-{event.user_id}')
    if right_answer:
        right_answer = right_answer.lower().replace('.', '*').replace('(', '*').split('*')[0].strip()

    if event.message_id == 1 or event.message.lower() == 'привет':
        user = vk_api.users.get(user_ids=event.user_id)[0]['first_name']
        message = f"Привет {user}!\nЧтобы начать викторину, нажми - «Новый вопрос»"
        send_message(event, vk_api, message, keyboard)

    elif event.message == 'Новый вопрос':
        random_question, random_answer = get_random_question()
        redis_db.set(f'vk-{event.user_id}', random_answer)
        send_message(event, vk_api, random_question, keyboard)

    elif event.message.lower() == right_answer:
        message = 'Правильно! Поздравляю! Для следующего вопроса нажми - «Новый вопрос»'
        send_message(event, vk_api, message, keyboard)

    elif event.message == 'Сдаться':
        message = f'Правильный ответ - {right_answer}\nДля продолжения нажми - «Новый вопрос»'
        send_message(event, vk_api, message, keyboard)

    else:
        message = 'Неверный ответ. Вы можете попробовать ещё раз'
        send_message(event, vk_api, message, keyboard)


def send_message(event, vk_api, message, keyboard):
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def main():
    chat_id = env.str('CHAT_ID')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(chat_id))
    logger.warning('VK_Quiz_Bot запущен.')
    redis_db = redis.Redis(
        host=env.str('REDIS_ENDPOINT'),
        port=env.str('REDIS_PORT'),
        db=0,
        password=env.str('REDIS_PASSWORD'),
        decode_responses=True
    )
    vk_session = vk.VkApi(token=env.str('VK_TOKEN'))
    vk_api = vk_session.get_api()
    keyboard = create_keyboard()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_bot(event, vk_api, keyboard, redis_db)


if __name__ == "__main__":
    main()
