import os
from typing import Coroutine

import requests

from config import NEW_DIR_PATH, NEW_FILE_PATH
from utils import coroutine


@coroutine
def create_directory() -> Coroutine:
    """Function create directory"""
    try:
        while True:
            yield
            os.mkdir(NEW_DIR_PATH)
            print(f"Директория {NEW_DIR_PATH} создана")
    except FileExistsError:
        print(f"Директория {NEW_DIR_PATH} уже существует")
        raise


@coroutine
def create_file():
    try:
        while True:
            yield
            with open(NEW_FILE_PATH, "w") as file:
                file.write("Test file hello")
            print(f"Файл {NEW_FILE_PATH} создан")
    except Exception as error:
        print(f"Ошибка при создании файла {NEW_FILE_PATH}: {error}")
        raise


@coroutine
def get_request():
    url = "http://yandex.ru"
    try:
        while True:
            yield
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


@coroutine
def hello_world():
    while True:
        yield
        print("hello world task")

@coroutine
def hello_world_2():
    while True:
        yield
        print("hello world_2 task")

@coroutine
def hello_world_3():
    while True:
        yield
        print("hello world_3 task")