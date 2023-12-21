from bs4 import BeautifulSoup
import cloudscraper
import re


class HelikonScraper:
    def __init__(self, search_term):
        self.individual_search_items = set()
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        url = f"https://g.helikon.bg/search/?q={search_term}"
        response = self.scraper.get(url)

        if response.status_code == 200:
            html_content = response.content
            self.extract_individual_search_items(html_content, search_term)
            self.get_book_info()
        else:
            print("Failed to fetch the page:", response.status_code)

    def extract_individual_search_items(self, html_content, search_term):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_items = soup.select("div.col-sm-4.col-md-3.col-xs-6")

        for item in product_items:
            a_tag = item.find('h5', class_='product-caption-title').find('a')
            title = a_tag.text
            processed_title = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', title)).strip()

            if search_term.lower() in processed_title.lower():
                href = a_tag.get('href')
                self.individual_search_items.add(href)

    def get_book_info(self):

        for item in self.individual_search_items:
            url = f"https://g.helikon.bg{item}"
            response = self.scraper.get(url)

            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')

                book_details = self.extract_book_details(soup)
                formatted_details = self.format_book_details(book_details)
                print(formatted_details)

            else:
                print("Failed to fetch the page:", response.status_code)

    @staticmethod
    def extract_book_details(soup):
        book_details = {}

        box_highlight = soup.find(class_='_box-highlight')
        if box_highlight:
            book_details["book_title"] = box_highlight.find('h3').text.strip()
            author_tag = box_highlight.find('h5')
            if author_tag:
                book_details["author"] = author_tag.text.strip('Автор: ')

        image_source = soup.find(class_='popup-gallery-image')
        if image_source:
            book_details["img_src"] = image_source.find('img')['src']

        tab_content_div = soup.find('div', class_='tab-pane fade in active', id='annotation')
        if tab_content_div:
            book_details["description"] = tab_content_div.get_text(separator=' ', strip=True)

        html_data = soup.find_all('table')
        for html_table in html_data:
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
        return book_details

    @staticmethod
    def format_book_details(book_details):
        formatted_details = {
            "book_title": book_details.get("book_title", ""),
            "author": book_details.get("author", ""),
            "publisher": book_details.get("publisher", ""),
            "ISBN": book_details.get("ISBN", ""),
            "language": book_details.get("language", ""),
            "publication_year": book_details.get("publication_year", ""),
            "img_src": book_details.get("img_src", ""),
            "tags": book_details.get("tags", ""),
            "description": book_details.get("description", "")
        }
        return formatted_details
