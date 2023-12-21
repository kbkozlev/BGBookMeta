from helikon import HelikonScraper
from orange import OrangeScraper

search_term = 'Бог пътува винаги инкогнито'

if __name__ == "__main__":
    HelikonScraper(search_term)
    OrangeScraper(search_term)
