from helikon import HelikonScraper
from orange import OrangeScraper

search_term = 'Сойка Присмехулка'

if __name__ == "__main__":
    HelikonScraper(search_term)
    OrangeScraper(search_term)

