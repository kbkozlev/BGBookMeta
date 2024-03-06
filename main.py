import time
from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper
from scrapers.biblioman import BibliomanScraper
import concurrent.futures
from scrapers.helpers.utils import clear_screen
from advancedprinter import print, line, input
import threading


def fetch_books_from_scraper(scraper):
    try:
        return scraper.get_book_list()
    except Exception as e:
        print(f"Error fetching books from {type(scraper).__name__}: {e}", c='red')
        return []


def search_progress():
    print("\nSearching, please wait", end='', flush=True)
    while not search_completed:
        for _ in range(3):
            print(".", end='', flush=True)
            time.sleep(0.5)
        print("\b\b\b   \b\b\b", end='', flush=True)  # Clearing the dots
        time.sleep(0.5)


def main():
    global search_completed
    while True:
        clear_screen()
        start_time = time.time()

        search_term = input("Book Title: ", c='blue1')  # or 'Сойка-Присмехулка'  # Remove first comment for testing purposes

        searching_thread = threading.Thread(target=search_progress)
        searching_thread.start()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(fetch_books_from_scraper, HelikonScraper(search_term)),
                executor.submit(fetch_books_from_scraper, OrangeScraper(search_term)),
                executor.submit(fetch_books_from_scraper, PazarScraper(search_term)),
                executor.submit(fetch_books_from_scraper, BibliomanScraper(search_term))
            ]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

            # Retrieve results
            books_from_helikon, books_from_orange, books_from_pazar, books_from_biblioman = [future.result() for future
                                                                                             in futures]

        search_completed = True
        searching_thread.join()  # Wait for the search thread to finish
        print("\b \b" * 30, end='', flush=True)  # Used to clear the 'Searching' text

        all_books = books_from_biblioman + books_from_helikon + books_from_orange + books_from_pazar

        for i, book in enumerate(all_books, start=1):
            print(f"Book {i}:", c='green2')
            for key, value in book.items():
                print(f"""{line(f'{key}', c='cyan')}: {value}""")

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"""\n{line(f"Execution time:", c='blue1')} {round(execution_time)}s""")

        exit_check = input("\nPress Enter to continue or 'exit': ", c='yellow')
        if exit_check.strip() == 'exit':
            break


if __name__ == "__main__":
    search_completed = False
    main()
