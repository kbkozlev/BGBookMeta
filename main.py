from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper


class BookScraperManager:
    def __init__(self, *scrapers):
        self.scrapers = list(scrapers)

    def fetch_books(self):
        all_books = []

        for scraper in self.scrapers:
            try:
                all_books.extend(scraper.get_book_list())
            except Exception as e:
                print(f"Error fetching books from {type(scraper).__name__}: {e}")

        return all_books


if __name__ == "__main__":
    search_term = ('не пипай тази книга')

    helikon = HelikonScraper(search_term)
    orange = OrangeScraper(search_term)
    pazar = PazarScraper(search_term)

    scraper_manager = BookScraperManager(helikon, orange, pazar)
    books = scraper_manager.fetch_books()

    for i, book in enumerate(books, start=1):
        print(f"Book {i}:")
        for key, value in book.items():
            print(f'{key}: {value}')
        print()
