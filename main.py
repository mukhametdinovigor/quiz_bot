import os
import re

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


env = Env()
env.read_env()


def start(update, context):
    user = update.message.from_user.username
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    update.message.reply_text(
        text=f"Привет {user}!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )


def echo(update, context):
    update.message.reply_text(update.message.text)


def get_questions(question_folder='questions'):
    questions = dict()
    question_files = os.listdir(question_folder)
    for question_file in question_files:
        with open(f"{question_folder}/{question_file}", "r", encoding='KOI8-R') as file:
            question_file_contents = file.read()
            questions_answers = re.split(r'Вопрос+[a-zA-Z0-9 ]+:', question_file_contents)[1:]
            for question_answer in questions_answers:
                question, answer = re.split(r'Ответ:', question_answer)
                questions[question.strip()] = answer.strip().split('\n')[0]
    return questions


def main():
    questions = get_questions()

    updater = Updater(env.str("TG_TOKEN"))
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == main():
    main()
