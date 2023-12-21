from helikon import HelikonScraper
from orange import OrangeScraper
from knizhenPazar import PazarScraper

search_term = ('Един наивник на средна възраст. Реквием за една мръсница')

if __name__ == "__main__":
    #HelikonScraper(search_term)
    #OrangeScraper(search_term)
    PazarScraper(search_term)
