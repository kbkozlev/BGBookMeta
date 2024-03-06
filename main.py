import time
from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper
from scrapers.biblioman import BibliomanScraper
import concurrent.futures
from scrapers.helpers.utils import clear_screen
from advancedprinter import print, line, input


def fetch_books_from_scraper(scraper):
    try:
        return scraper.get_book_list()
    except Exception as e:
        print(f"Error fetching books from {type(scraper).__name__}: {e}", c='red')
        return []


def main():
    while True:
        clear_screen()
        start_time = time.time()

        search_term = input("Book Title: ", c='blue1')  # or 'Сойка-Присмехулка'  # Remove first comment for testing purposes

        with concurrent.futures.ThreadPoolExecutor() as executor:
            books_from_helikon = executor.submit(fetch_books_from_scraper, HelikonScraper(search_term)).result()
            books_from_orange = executor.submit(fetch_books_from_scraper, OrangeScraper(search_term)).result()
            books_from_pazar = executor.submit(fetch_books_from_scraper, PazarScraper(search_term)).result()
            books_from_biblioman = executor.submit(fetch_books_from_scraper, BibliomanScraper(search_term)).result()

        all_books = books_from_biblioman + books_from_helikon + books_from_orange + books_from_pazar

        for i, book in enumerate(all_books, start=1):
            print(f"\nBook {i}:", c='green2')
            for key, value in book.items():
                print(f"""{line(f'{key}', c='cyan')}: {value}""")

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"""\n{line(f"Execution time:", c='blue1')} {round(execution_time)}s""")

        exit_check = input("\nPress Enter to continue or 'exit': ", c='yellow')
        if exit_check.strip() == 'exit':
            break


if __name__ == "__main__":
    main()
