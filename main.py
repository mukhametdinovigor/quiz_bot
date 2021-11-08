from environs import Env
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from get_questions import get_questions

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
    update.message.reply_text('question')


def send_count(update, context):
    update.message.reply_text('count')





def main():
    questions = get_questions()

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
