import json
import argparse

from dialogflow_utils import create_intent

from environs import Env


def get_user_args():
    parser = argparse.ArgumentParser(
        description='Teaches the DialogueFlow new phrases'
    )
    parser.add_argument(
        '-f', '--filepath', default='questions.json',
        help='Path to the file with new phrases'
        )

    args = parser.parse_args()

    return args


def read_file(filename):
    with open(filename, 'r') as my_file:
        file_content = json.loads(my_file.read())

    return file_content


def main():
    env = Env()
    env.read_env()
    project_id = env.str('DIALOD_ID')

    args = get_user_args()
    filepath = args.filepath

    intents = read_file(filepath)
    for intent, intent_content in intents.items():
        questions = intent_content['questions']
        answer = intent_content['answer']

        create_intent(
            project_id=project_id,
            display_name=intent,
            training_phrases_parts=questions,
            message_texts=[answer])


if __name__ == '__main__':
    main()
