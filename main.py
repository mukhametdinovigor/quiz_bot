from environs import Env
import redis
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from question_tools import get_random_questions

env = Env()
env.read_env()

NEW_QUESTION, ATTEMPT, COUNT = range(3)

REDIS_DB = redis.Redis(
    host=env.str('REDIS_ENDPOINT'),
    port=env.str('REDIS_PORT'),
    db=0,
    password=env.str('REDIS_PASSWORD'),
    decode_responses=True
)


def start(update, context):
    user = update.message.from_user.username
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    update.message.reply_text(
        text=f"Привет {user}!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True
        ),
    )
    return NEW_QUESTION


def handle_new_question_request(update, context):
    random_question, random_answer = get_random_questions()
    print(random_answer)
    REDIS_DB.set(update.message.chat_id, random_question)
    REDIS_DB.set(random_question, random_answer)
    update.message.reply_text(random_question)
    return ATTEMPT


def handle_solution_attempt(update, context):
    question_for_check = REDIS_DB.get(update.message.chat_id)
    answer = REDIS_DB.get(question_for_check)
    right_answer = answer.replace('.', '*').replace('(', '*').split('*')[0].strip()
    print(right_answer)
    if update.message.text == right_answer:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми - «Новый вопрос»')
        return NEW_QUESTION
    update.message.reply_text('Неверный ответ. Вы можете попробовать ещё раз')


def handle_give_up(update, context):
    question_for_check = REDIS_DB.get(update.message.chat_id)
    answer = REDIS_DB.get(question_for_check)
    right_answer = answer.replace('.', '*').replace('(', '*').split('*')[0].strip()
    update.message.reply_text(f'Правильный ответ - {right_answer}\nДля продолжения нажми - «Новый вопрос»')
    return NEW_QUESTION


def send_count(update, context):
    update.message.reply_text('count')


def main():
    updater = Updater(env.str("TG_TOKEN"))
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        allow_reentry=True,
        states={
            NEW_QUESTION: [MessageHandler(Filters.regex('^(Новый вопрос)$'), handle_new_question_request)],
            COUNT: [MessageHandler(Filters.regex('^(Мой счёт)$'), send_count)],
            ATTEMPT: [
                MessageHandler(Filters.text('Сдаться'), handle_give_up),
                MessageHandler(Filters.text, handle_solution_attempt)],

        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == main():
    main()
