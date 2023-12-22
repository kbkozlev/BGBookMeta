from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper

search_term = 'Сойка Присмехулка'


def print_books(*args):
    full_list = []

    for scraper in args:
        full_list.extend(scraper.get_book_list())

    max_key_length = max(len(key) for book in full_list for key in book.keys())
    i = 1

    for book in full_list:
        print(f'Book Nr.{i}')
        print('------------')
        for key, value in book.items():
            print(f"{key.ljust(max_key_length)}: {value}")
        i+=1
        print()

    print(f"Total books fetched: {len(full_list)}")
    print("========================")


if __name__ == "__main__":
    helikon = HelikonScraper(search_term)
    orange = OrangeScraper(search_term)
    pazar = PazarScraper(search_term)

    print_books(helikon, orange, pazar)
