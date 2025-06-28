from src.utils import get_information_from_json, get_events_information


def get_inform_for_veb_page(date_str: str, data_range: str) -> tuple:
    """Выводит JSON-строку для страницы 'Главная'"""
    inform_for_home_page = get_information_from_json(date_str)

    events_information = get_events_information(date_str, data_range)

    return inform_for_home_page, events_information
