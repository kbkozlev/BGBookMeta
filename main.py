import time
import threading
import concurrent.futures
from src.scrapers.helikon import HelikonScraper
from src.scrapers.orange import OrangeScraper
from src.scrapers.knizhenPazar import PazarScraper
from src.scrapers.biblioman import BibliomanScraper
from advancedprinter import print, line, input
from src.helpers.utils import clear_screen


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
    print("\b \b" * 30, end='', flush=True)  # Used to clear the 'Searching' text
    print("\033[F", end='')  # Move one line up


def main():
    global search_completed

    while True:
        clear_screen()
        search_completed = False
        # Remove comment below for testing purposes
        search_term = input("Book Title: ", c='blue1')  # or 'Сойка-Присмехулка'

        if search_term.strip() != '':
            searching_thread = threading.Thread(target=search_progress)
            searching_thread.start()

            start_time = time.time()

            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(fetch_books_from_scraper, HelikonScraper(search_term)),  # Issues with cloudflare
                        executor.submit(fetch_books_from_scraper, OrangeScraper(search_term)),
                        executor.submit(fetch_books_from_scraper, PazarScraper(search_term)),
                        executor.submit(fetch_books_from_scraper, BibliomanScraper(search_term))
                    ]
                    # TODO: To add more scrapers - www.goodreads.com

                    # Wait for all tasks to complete
                    concurrent.futures.wait(futures)

                    # Retrieve results
                    all_books = []
                    for future in concurrent.futures.as_completed(futures):
                        all_books.extend(future.result())

            except Exception as e:
                print(e)
                break

            finally:
                search_completed = True
                searching_thread.join()  # Wait for the search thread to finish

            # Sort all_books based on the number of non-empty values
            sorted_books = sorted(all_books, key=lambda books: sum(3 if k.lower() == "description" and len(str(val)) > 1 else 1 if len(
                str(val)) > 1 else 0 for k, val in books.items()), reverse=True)

            for i, book in enumerate(sorted_books, start=1):
                print(f"\nBook {i}:", c='green2')
                for key, value in book.items():
                    print(f"""{line(f'{key}', c='cyan')}: {value}""")

            end_time = time.time()
            execution_time = end_time - start_time
            minutes = int(execution_time // 60)
            seconds = int(execution_time % 60)

            time_text = f"{line(f'Execution time:', c='blue1')}"
            print(f"""\n{time_text} {minutes}m {seconds}s""" if minutes > 0 else f"""\n{time_text} {seconds}s""")

        exit_check = input("\nPress Enter to continue or 'e' to exit: ", c='yellow')
        if exit_check.strip().lower() != '':
            break


if __name__ == "__main__":
    search_completed: bool
    main()
