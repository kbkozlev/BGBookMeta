import time
from scrapers.helikon import HelikonScraper
from scrapers.orange import OrangeScraper
from scrapers.knizhenPazar import PazarScraper
from scrapers.biblioman import BibliomanScraper
import concurrent.futures


def fetch_books_from_scraper(scraper):
    try:
        return scraper.get_book_list()
    except Exception as e:
        print(f"Error fetching books from {type(scraper).__name__}: {e}")
        return []


if __name__ == "__main__":
    start_time = time.time()  # Record the start time

    search_term = 'Хари Потър и стаята на тайните'

    helikon = HelikonScraper(search_term)
    orange = OrangeScraper(search_term)
    pazar = PazarScraper(search_term)
    biblioman = BibliomanScraper(search_term)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submitting tasks for execution
        future_helikon = executor.submit(fetch_books_from_scraper, helikon)
        future_orange = executor.submit(fetch_books_from_scraper, orange)
        future_pazar = executor.submit(fetch_books_from_scraper, pazar)
        future_biblioman = executor.submit(fetch_books_from_scraper, biblioman)

        # Retrieve results
        books_from_helikon = future_helikon.result()
        books_from_orange = future_orange.result()
        books_from_pazar = future_pazar.result()
        books_from_biblioman = future_biblioman.result()

    all_books = books_from_helikon + books_from_orange + books_from_pazar + books_from_biblioman

    for i, book in enumerate(all_books, start=1):
        print(f"Book {i}:")
        for key, value in book.items():
            print(f'{key}: {value}')
        print()

    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate execution time
    print(f"Execution time: {execution_time} seconds")
