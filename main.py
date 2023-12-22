from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper


search_term = 'Сойка Присмехулка'


def print_books(*args):
    full_list = []

    for scraper in args:
        full_list.extend(scraper.get_book_list())

    for book in full_list:
        print(book)


if __name__ == "__main__":
    helikon = HelikonScraper(search_term)
    orange = OrangeScraper(search_term)
    pazar = PazarScraper(search_term)

    print_books(helikon, orange, pazar)
