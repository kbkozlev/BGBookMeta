from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper

search_term = 'Сойка присмехулка'


def print_books(*scrapers):
    all_books = []

    for scraper in scrapers:
        try:
            books = scraper.get_book_list()
            all_books.extend(books)
        except Exception as e:
            print(f"Error fetching books from {type(scraper).__name__}: {e}")

    if all_books:
        max_key_length = max(len(key) for book in all_books for key in book.keys())

        for idx, book in enumerate(all_books, start=1):
            print(f'Book Nr.{idx}')
            print('------------')
            for key, value in book.items():
                print(f"{key.ljust(max_key_length)}: {value}")
            print()

        print(f"Total books fetched: {len(all_books)}")
    else:
        print("No books fetched from any scraper.")
    print("==================================")


if __name__ == "__main__":
    helikon = HelikonScraper(search_term)
    orange = OrangeScraper(search_term)
    pazar = PazarScraper(search_term)

    print_books(helikon, orange, pazar)
