import os

from src.reports import spending_by_category
from src.services import get_search
from src.utils import get_data_for_analytic, get_dict, get_operation_file, get_settings
from src.views import final_json

current_dir = os.path.dirname(os.path.dirname(__file__))  # пути к файлу эксель
xls_path = os.path.join(current_dir, "data", "operations_example.xls")
json_path = os.path.join(current_dir, "data", "user_settings.json")


def main():
    transactions_df = get_operation_file(xls_path)
    print(get_operation_file(xls_path))
    transactions_dict = get_dict(transactions_df)
    users_settings = get_settings(json_path)
    users_date = input("Введите дату для анализа операций в формате дд.мм.гггг: ").strip()
    transactions_data = get_data_for_analytic(transactions_dict, users_date)
    print(final_json(transactions_data, users_settings))
    user_request = input("Для поиска операции, введите ключевое слово: ").strip()
    print(get_search(transactions_dict, user_request))
    user_category = input("Выберите категорию: ").strip()
    spending_by_category(transactions_df, user_category, users_date)
    print("Отчет сохранен в файл")


if __name__ == "__main__":
    main()
