import os
import re


def get_questions(question_folder='questions'):
    questions = dict()
    question_files = os.listdir(question_folder)
    for question_file in question_files:
        with open(f"{question_folder}/{question_file}", "r", encoding='KOI8-R') as file:
            question_contents = file.read()
            questions_answers = re.split(r'Вопрос+[a-zA-Z0-9 ]+:', question_contents)[1:]
            for question_answer in questions_answers:
                question, answer = re.split(r'Ответ:', question_answer)
                questions[question.strip()] = answer.strip().split('\n')[0]
    return questions


def main():
    questions = get_questions()
    print(questions)


if __name__ == main():
    main()
