import os
import random
import re


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


def get_random_questions():
    questions = get_questions()
    random_question, random_answer = random.choice(list(questions.items()))
    random_question = random_question.replace('\n', ' ').strip()
    return random_question, random_answer
