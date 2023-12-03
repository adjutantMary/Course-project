import json
import os
from datetime import datetime
from typing import Any

import pandas as pd

current_dir = os.path.dirname(os.path.dirname(__file__))  # пути к файлу эксель
xls_path = os.path.join(current_dir, "data", "operations_example.xls")
json_path = os.path.join(current_dir, "data", "user_settings.json")


def get_operation_file(path: str) -> Any:
    """
    Функция для чтения файла operations_example.xls
    :param path: строка с путем до файла
    :return: DataFrame
    """
    data = pd.read_excel(path)
    return data


def get_dict(df: pd.DataFrame) -> list:
    """
    Функция принимает DataFrame и преобразует его в словарь операций
    :param df: DataFrame
    :return: словарь операций
    """
    list_operations = df.to_dict(orient="records")
    return list_operations


def get_settings(file: str) -> dict:
    """
    Функция принимает путь JSON-файла с пользовательскими настройками и возвращает словарь с настройками
    :param file: путь до JSON-файла
    :return: словарь dict с настройками
    """
    with open(file, encoding="utf-8") as f:
        setting: dict = json.load(f)
    return setting


def get_data_for_analytic(transactions: list[dict], time: str) -> list[dict]:
    """
    Функция возвращает операции в определенном установленном промежутке времени.
    Данные для анализа и вывода на веб-страницах — это данные с начала месяца,
    на который выпадает входящая дата, по входящую дату.
    :param transactions: list[dict] список всех транзакций.
    :param time: указанная дата формата дд.мм.гг.
    :return: list[dict] список всех операций, которые входят в промежуток
    """
    current_time = datetime.strptime(time, "%d.%m.%Y")
    day = current_time.day
    month = current_time.month
    year = current_time.year
    correct_operations = []

    for operation in transactions:
        operation_time = datetime.strptime(
            operation["Дата операции"], "%d.%m.%Y %H:%M:%S"
        )
        if (
            operation_time.month == month
            and operation_time.year == year
            and day >= operation_time.day >= 1
            and operation["Статус"] == "OK"
        ):
            correct_operations.append(operation)

    return correct_operations


operation = get_operation_file(xls_path)
operation_dict = get_dict(operation)
# print(get_settings(json_path))
data = get_data_for_analytic(operation_dict, '30.09.2020')
# # # print(len(get_data_for_analytic(operation_dict, '03.12.2023')))
