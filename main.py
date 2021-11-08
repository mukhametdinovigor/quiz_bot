from environs import Env
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from question_tools import get_random_questions

env = Env()
env.read_env()

THING, CHOOSING = range(2)


def start(update, context):
    user = update.message.from_user.username
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    update.message.reply_text(
        text=f"Привет {user}!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True
        ),
    )
    return CHOOSING


def send_question(update, context):
    random_question, random_answer = get_random_questions()
    update.message.reply_text(random_question)


def send_count(update, context):
    update.message.reply_text('count')


def main():
    updater = Updater(env.str("TG_TOKEN"))
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        allow_reentry=True,
        states={
            CHOOSING:
                [
                    MessageHandler(
                        Filters.regex('^(Новый вопрос)$'),
                        send_question
                    ),
                    MessageHandler(
                        Filters.regex('^(Мой счёт)$'),
                        send_count
                    )
                ],
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == main():
    main()
