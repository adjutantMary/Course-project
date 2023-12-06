import datetime
import json

from src.check_api import get_currency, get_stocks


def get_greetings() -> str:
    """
    Функция возвращает приветствие в формате “Добрый ???”, где ??? - утро/день/вечер/ночь
    в зависимости от текущего времени с помощью модуля datetime
    :return: str
    """
    current_time = datetime.datetime.now()
    hours_string = current_time.strftime("%H")

    if 4 <= int(hours_string) < 12:
        return "Доброе утро"
    elif 12 <= int(hours_string) < 18:
        return "Добрый день"
    elif 18 <= int(hours_string) <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card(operations: list[dict]) -> list[dict]:
    """
    Функция возвращает список словарей, который содержит информацию о сумме всех операций,
    и кэшбек, полученный в ходе данных операций
    :param operations:list[dict] со всеми операциями
    :return: list[dict] c указанной информацией
    """
    unique_cards = set([x["Номер карты"] for x in operations if str(x["Номер карты"]) != "nan"])
    operation_list = []

    for card in unique_cards:
        summ = -sum([x["Сумма операции"] for x in operations if x["Сумма операции"] < 0 and x["Номер карты"] == card])
        round_sum = round(summ, 2)
        cashback = int(round_sum / 100)

        card_info = {
            "last_digits": card[1:],
            "total_spent": round_sum,
            "cashback": cashback,
        }
        operation_list.append(card_info)
    return operation_list


def top_five_operations(operations: list[dict]) -> list[dict]:
    """
    Функция, в ходе обработки списка финансовых операций, сортирует и возвращает топ-5 операций,
    которые имеют наибольшие суммы операций
    :param operations: list[dict] список всех банковских операций
    :return: list[dict] список топ-5 операций
    """
    all_operations = []
    sorted_operations = sorted(operations, key=lambda x: abs(x["Сумма операции"]), reverse=True)
    if len(sorted_operations) >= 5:
        top_operations = sorted_operations[0:5]
    else:
        top_operations = sorted_operations
    for operation in top_operations:
        operation_info = {
            "date": operation["Дата операции"],
            "amount": operation["Сумма операции"],
            "category": operation["Категория"],
            "description": operation["Описание"],
        }
        all_operations.append(operation_info)
    return all_operations


def final_json(operations: list[dict], settings: dict) -> str:
    """
    Функция, которая возвращает итоги со всех функций в виде JSON - фидбэка (файла) в виде словаря dict
    :param operations: list[dict] список всех операций
    :param settings: пользовательские настройки
    :return: итоговый JSON-словарь с операциями (фидбек)
    """
    json_dict = {
        "greeting": get_greetings(),
        "cards": get_card(operations),
        "top_transactions": top_five_operations(operations),
        "currency_rates": get_currency(settings["user_currencies"]),
        "stock_prices": get_stocks(settings["user_stocks"]),
    }
    json_file = json.dumps(json_dict, ensure_ascii=False, indent=2)

    return json_file
