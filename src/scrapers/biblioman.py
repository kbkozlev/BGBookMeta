from bs4 import BeautifulSoup
import cloudscraper
from src.helpers.utils import format_book_details, process_title_text


class BibliomanScraper:
    def __init__(self, search_term):
        self.formatted_details = []
        self.individual_search_items = set()
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        url = f"https://biblioman.chitanka.info/books?q={search_term}"
        response = self.scraper.get(url)

        if response.status_code == 200:
            html_content = response.content
            self.__extract_individual_search_items(html_content, search_term)
            self.__get_book_info()
        else:
            print(f"{self.__class__.__name__} failed to fetch the main page: {response.status_code}")

    def __extract_individual_search_items(self, html_content, search_term):
        soup = BeautifulSoup(html_content, 'html.parser')
        book_items = soup.select("div.col-xs-12.col-md-6")

        for item in book_items:
            a_tag = item.find('div', class_='book-title-and-author').find('a')
            processed_title = process_title_text(a_tag.text.strip())
            search = process_title_text(search_term)

            if search in processed_title:
                href = a_tag['href']
                self.individual_search_items.add(href)

    def __get_book_info(self):

        for item in self.individual_search_items:
            url = f"https://biblioman.chitanka.info{item}"
            response = self.scraper.get(url)

            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')

                book_details = {
                    "book_title": soup.find(class_='col-md-8 entity-field entity-field-title').find('a').text.strip(),
                    "author": soup.find(class_='col-md-8 entity-field entity-field-author').find('a').text.rstrip(),
                    "img_src": "https://biblioman.chitanka.info/" +
                               soup.find('a', class_='thumb-link')['href'].split('.jpg')[0] + '.jpg',
                    "description": ''.join(p.get_text(strip=True) for p in
                                           soup.find(class_='col-md-8 entity-field entity-field-annotation').find_all('p'))
                    if soup.find(class_='col-md-8 entity-field entity-field-annotation') else '',
                    "publisher": soup.find(class_='col-md-8 entity-field entity-field-publisher').find('a').text.strip(),
                    "language": soup.find(class_='col-md-8 entity-field entity-field-language').find('a').text.strip(),
                    "publication_year": soup.find(class_='col-md-8 entity-field entity-field-publishingYear').find('a').text.strip(),
                    "ISBN": (soup.find(class_='col-md-8 entity-field entity-field-isbn').find('a').text.replace('-', '')
                             .strip() if (soup.find(class_='col-md-8 entity-field entity-field-isbn')
                                          and soup.find(class_='col-md-8 entity-field entity-field-isbn').find('a')) else ""),
                    "tags": soup.find(class_='col-md-8 entity-field entity-field-category').find('a').text.strip(),
                    }

                self.__format_book_details(book_details)

            else:
                print(f"{self.__class__.__name__} failed to fetch {url}: {response.status_code}")

    def __format_book_details(self, book_details):
        formatted_details = format_book_details(book_details)
        self.formatted_details.append(formatted_details)

    def get_book_list(self):
        return self.formatted_details
