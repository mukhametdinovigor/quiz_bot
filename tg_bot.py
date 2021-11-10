import logging

from environs import Env
import redis
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup

from quiz_questions import get_random_question
from tg_logs_handler import TelegramLogsHandler

logger = logging.getLogger('Logger')
env = Env()
env.read_env()

NEW_QUESTION, ATTEMPT, COUNT = range(3)


def start(update, context):
    user = update.message.from_user.username
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    update.message.reply_text(
        text=f"Привет {user}!\nЧтобы начать викторину, нажми - «Новый вопрос»",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True
        ),
    )
    return NEW_QUESTION


def handle_new_question_request(update, context):
    redis_db = redis.Redis(
        host=env.str('REDIS_ENDPOINT'),
        port=env.str('REDIS_PORT'),
        db=0,
        password=env.str('REDIS_PASSWORD'),
        decode_responses=True
    )
    context.user_data['redis_db'] = redis_db
    random_question, random_answer = get_random_question()
    redis_db.set(f'tg-{update.message.chat_id}', random_question)
    redis_db.set(random_question, random_answer)
    update.message.reply_text(random_question)
    return ATTEMPT


def handle_solution_attempt(update, context):
    question_for_check = context.user_data['redis_db'].get(f'tg-{update.message.chat_id}')
    answer = context.user_data['redis_db'].get(question_for_check)
    right_answer = answer.lower().replace('.', '*').replace('(', '*').split('*')[0].strip()
    if update.message.text.lower() == right_answer:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми - «Новый вопрос»')
        return NEW_QUESTION
    update.message.reply_text('Неверный ответ. Вы можете попробовать ещё раз')


def handle_give_up(update, context):
    question_for_check = context.user_data['redis_db'].get(f'tg-{update.message.chat_id}')
    answer = context.user_data['redis_db'].get(question_for_check)
    right_answer = answer.lower().replace('.', '*').replace('(', '*').split('*')[0].strip()
    update.message.reply_text(f'Правильный ответ - {right_answer}\nДля продолжения нажми - «Новый вопрос»')
    return NEW_QUESTION


def main():
    chat_id = env.str('CHAT_ID')
    updater = Updater(env.str("TG_TOKEN"))
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(chat_id))
    logger.warning('TG_Quiz_Bot запущен.')

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        allow_reentry=True,
        states={
            NEW_QUESTION: [MessageHandler(Filters.regex('^(Новый вопрос)$'), handle_new_question_request)],
            ATTEMPT: [
                MessageHandler(Filters.regex('^(Сдаться)$'), handle_give_up),
                MessageHandler(Filters.text, handle_solution_attempt)],
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == main():
    main()
