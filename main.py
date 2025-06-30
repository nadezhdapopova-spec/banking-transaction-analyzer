from src.views import get_inform_for_veb_page

def main() -> None:
    """Выводит JSON-ответы"""
    home_page_inform, events_inform = get_inform_for_veb_page("2021-12-31 22:39:04", "W")

    print(home_page_inform)
    print(events_inform)


if __name__ == "__main__":
    main()
