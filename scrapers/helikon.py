from bs4 import BeautifulSoup
import cloudscraper
import re
from .helpers.utils import format_book_details


class HelikonScraper:
    def __init__(self, search_term):
        self.formatted_details = []
        self.individual_search_items = set()
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        url = f"https://g.helikon.bg/search/?q={search_term}"
        response = self.scraper.get(url)

        if response.status_code == 200:
            html_content = response.content
            self.__extract_individual_search_items(html_content, search_term)
            self.__get_book_info()
        else:
            print("Failed to fetch the page:", response.status_code)

    def __extract_individual_search_items(self, html_content, search_term):
        soup = BeautifulSoup(html_content, 'html.parser')
        book_items = soup.select("div.col-sm-4.col-md-3.col-xs-6")

        for item in book_items:
            a_tag = item.find('h5', class_='product-caption-title').find('a')
            processed_title = re.sub(r'\s+', ' ', re.sub(r'[^\w\s.]', ' ', a_tag.text)).strip()

            if search_term.lower() in processed_title.lower():
                href = a_tag.get('href')
                self.individual_search_items.add(href)

    def __get_book_info(self):

        for item in self.individual_search_items:
            url = f"https://g.helikon.bg{item}"
            response = self.scraper.get(url)

            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')

                book_details = {"book_title": soup.find(class_='_box-highlight').find('h3').text.strip(),
                                "author": soup.find(class_='_box-highlight').find('h5').text.strip('Автор: '),
                                "img_src": soup.find(class_='popup-gallery-image').find('img')['src'],
                                "description": soup.find('div', class_='tab-pane fade in active',
                                                         id='annotation').get_text(
                                    separator=' ', strip=True)}

                for html_table in soup.find_all('table'):
                    table_rows = html_table.find_all('tr')
                    for row in table_rows:
                        cells = row.find_all('td')
                        if len(cells) == 2:
                            key = cells[0].text.strip()
                            value = cells[1].text.strip()
                            key_mapping = {
                                'Издател': 'publisher',
                                'Език': 'language',
                                'Година на издаване': 'publication_year',
                                'ISBN': 'ISBN',
                                'Категории': 'tags',
                            }
                            if key in key_mapping:
                                book_details[key_mapping[key]] = value

                self.__format_book_details(book_details)

            else:
                print("Failed to fetch the page:", response.status_code)

    def __format_book_details(self, book_details):
        formatted_details = format_book_details(book_details)
        self.formatted_details.append(formatted_details)

    def get_book_list(self):
        return self.formatted_details
