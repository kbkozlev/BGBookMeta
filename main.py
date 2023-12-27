from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper


def fetch_books_from_scrapers(*scrapers):
    all_books = []

    for scraper in scrapers:
        try:
            all_books.extend(scraper.get_book_list())
        except Exception as e:
            print(f"Error fetching books from {type(scraper).__name__}: {e}")

    return all_books


if __name__ == "__main__":
    search_term = ('Принц на нощта')

    helikon = HelikonScraper(search_term)
    orange = OrangeScraper(search_term)
    pazar = PazarScraper(search_term)

    books = fetch_books_from_scrapers(helikon, orange, pazar)

    for i, book in enumerate(books, start=1):
        print(f"Book {i}:")
        for key, value in book.items():
            print(f'{key}: {value}')
        print()
