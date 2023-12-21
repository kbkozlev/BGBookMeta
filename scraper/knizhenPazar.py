from bs4 import BeautifulSoup
import cloudscraper
import re

class PazarScraper:
    def __init__(self, search_term):
        self.individual_search_items = set()
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        url = f"https://knizhen-pazar.net/books/search?in=all&q={search_term}"
        response = self.scraper.get(url)

        if response.status_code == 200:
            html_content = response.content
            self.extract_individual_search_items(html_content, search_term)
            self.get_book_info()
        else:
            print("Failed to fetch the page:", response.status_code)

    def extract_individual_search_items(self, html_content, search_term):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_items = soup.find_all('div', class_='prl__item t_product')

        # Loop through each product item and extract details
        for item in product_items:
            a_tag = item.find('div', class_='prl__title').a
            title = a_tag.text
            processed_title = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', title)).strip()

            if search_term.lower() in processed_title.lower():
                href = a_tag.get('href')
                self.individual_search_items.add(href)

    def get_book_info(self):

        for item in self.individual_search_items:
            response = self.scraper.get(item)

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
        key_mapping = {
            'Издателство': 'publisher',
            'Език': 'language',
            'Година': 'publication_year',
            'ISBN': 'ISBN',
            'Категория': 'tags',
        }

        book_details = {
            "book_title": soup.find('h1', {'class': 'm_title margin_top_5 margin_bottom_0'}).get_text(),
            "author": soup.find('h2', {'class': 'margin_top_20 margin_bottom_5 no_b'}).get_text(),
        }

        img_tag = soup.find('img', class_='prdp__book_img')['src']
        book_details["img_src"] = img_tag

        labels = ['Издателство', 'Година', 'Език', 'ISBN', 'Категория']
        for label in labels:
            element = soup.find('div', text=label)
            if element:
                value = element.find_next_sibling('div', class_='prdp__value')
                if value:
                    key = key_mapping.get(label, label)  # Get the mapped key or use the original label
                    book_details[key] = value.get_text(strip=True)

        print(book_details)

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
        }
        return formatted_details