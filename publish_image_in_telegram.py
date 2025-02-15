﻿import argparse
import os
from pathlib import Path
import time

from dotenv import load_dotenv
import telegram
import telegram.error

import constants
from get_files import get_random_file


def create_parser():
    """ Создаёт парсер параметров командной строки. """

    parser = argparse.ArgumentParser(
            description='Публикует указанную или случайную (если не указана) '
                        'фотографию в telegram-канале.'
    )
    parser.add_argument(
        'image_filepath',
        nargs='?',
        help='путь к файлу с фото'
    )
    return parser


def publish_image_in_telegram(telegram_bot_token: str,
                              telegram_channel_id: str,
                              img_filepath: str):
    """
    Публикует указанную или случайную (если не указана) фотографию
    в указанном telegram-канале с помощью указанного telegram-бота.
    """

    bot = telegram.Bot(token=telegram_bot_token)

    delay = 1
    while True:
        try:
            bot.send_document(chat_id=telegram_channel_id,
                              document=open(img_filepath, 'rb'))
            return True
        except FileNotFoundError as ex:
            print(ex)
            print('Введён неправильный путь к файлу с фото.')
            return False
        except telegram.error.NetworkError as ex:
            print(ex)
            time.sleep(delay)
            delay = 10
        except Exception as ex:
            print(ex)
            return False


def main():
    load_dotenv()
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_channel_id = os.environ['TELEGRAM_CHANNEL_ID']

    parser = create_parser()
    args = parser.parse_args()

    if args.image_filepath:
        img_filepath = args.image_filepath
    else:
        img_dir = os.getenv('IMAGES_DIRECTORY',
                            default=constants.DEFAULT_IMAGES_DIRECTORY)
        img_dirpath = Path.cwd() / img_dir
        img_filepath = get_random_file(img_dirpath, recursive=True)

    if img_filepath:
        publish_image_in_telegram(telegram_bot_token, telegram_channel_id,
                                  img_filepath)


if __name__ == '__main__':
    main()
