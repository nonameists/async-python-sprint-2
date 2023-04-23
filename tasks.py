import os

import requests

from config import NEW_DIR_PATH, NEW_FILE_PATH
from utils import coroutine


def create_directory() -> None:
    """Function create directory"""
    try:
        os.mkdir(NEW_DIR_PATH)
        print(f"Директория {NEW_DIR_PATH} создана")
    except FileExistsError:
        print(f"Директория {NEW_DIR_PATH} уже существует")
        raise


def create_file():
    try:
        with open(NEW_FILE_PATH, "w") as file:
            file.write("Test file hello")
        print(f"Файл {NEW_FILE_PATH} создан")
    except Exception as error:
        print(f"Ошибка при создании файла {NEW_FILE_PATH}: {error}")
        raise


def get_request():
    url = "http://yandex.ru"
    try:
        response = requests.get(url)
        analyzer = analyze_response()
        analyzer.send(response)
    except Exception as error:
        print(f"Ошибка при обработкe {url}: {error}")
        raise


@coroutine
def analyze_response():
    while True:
        try:
            response = yield
            if response.status_code == 200:
                print("Успешный запрос")
            else:
                print(f"Ошибка {response.status_code}")
        except Exception as error:
            print(f"Ошибка при анализе ответа: {error}")


def hello_world():
    print("hello world task")

def hello_world_2():
    print("hello world_2 task")

def hello_world_3():
    print("hello world_3 task")