import os

from config import ROOT_DIR
from src.read_xlsx import read_transactions_excel
from src.reports import get_spending_by_category
from src.services import (
    get_profitable_cashback_categories,
    get_transactions_list,
    make_simple_search,
    search_for_transfers_to_individuals
)
from src.views import get_inform_for_veb_page


def main() -> None:
    """Выводит JSON-ответы"""
    home_page_inform, events_inform = get_inform_for_veb_page("2021-12-31 22:39:04", "W")

    transactions_list = get_transactions_list()
    profitable_cashback_categories = get_profitable_cashback_categories(transactions_list, month=11, year=2021)
    simple_search = make_simple_search("Ситидрайв")
    transfers_to_individuals_search = search_for_transfers_to_individuals(transactions_list)

    filepath = os.path.join(ROOT_DIR, "data", "operations.xlsx")
    transactions = read_transactions_excel(filepath)
    spending_by_category = get_spending_by_category(transactions, "Связь", "2021-12-30 22:39:04")

    print(home_page_inform)
    print(events_inform)

    print(profitable_cashback_categories)
    print(simple_search)
    print(transfers_to_individuals_search)

    print(spending_by_category)


if __name__ == "__main__":
    main()
