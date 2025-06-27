from src.utils import get_information_from_json


def get_inform_for_home_page(date_str: str) -> None:
    """Выводит JSON-строку для страницы 'Главная'"""
    information = get_information_from_json(date_str)

    print(information)


if __name__ == "__main__":
    get_inform_for_home_page("2021-12-31 22:39:04")
