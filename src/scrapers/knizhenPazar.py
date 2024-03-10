from bs4 import BeautifulSoup
import cloudscraper
from src.helpers.utils import format_book_details, process_title_text
import threading


class PazarScraper:
    def __init__(self, search_term):
        self.formatted_details = []
        self.individual_search_items = set()
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        url = f"https://knizhen-pazar.net/books/search?in=all&q={search_term}"
        response = self.scraper.get(url)

        if response.status_code == 200:
            html_content = response.content
            self.__extract_individual_search_items(html_content, search_term)
            self.__get_book_info_multithreaded()  # Change to use multithreaded method
        else:
            print(f"{self.__class__.__name__} failed to fetch the main page: {response.status_code}")

    def __extract_individual_search_items(self, html_content, search_term):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_items = soup.find_all('div', class_='prl__item t_product')

        for item in product_items:
            a_tag = item.find('div', class_='prl__title').a
            processed_title = process_title_text(a_tag.text)
            search = process_title_text(search_term)

            if search in processed_title:
                href = a_tag.get('href')
                self.individual_search_items.add(href)

    def __get_book_info(self, item):
        response = self.scraper.get(item)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            book_details = {
                "book_title": soup.find('h1', {'class': 'm_title margin_top_5 margin_bottom_0'}).get_text(),
                "author": soup.find('h2', {'class': 'margin_top_20 margin_bottom_5 no_b'}).get_text()
                if soup.find('h2', {'class': 'margin_top_20 margin_bottom_5 no_b'}) else "",
                "img_src": '' if soup.find('img', class_='prdp__book_img')['src'].startswith('/assets/') else
                soup.find('img', class_='prdp__book_img')['src']
            }

            key_mapping = {
                'Издателство': 'publisher',
                'Език': 'language',
                'Година': 'publication_year',
                'ISBN': 'ISBN',
                'Категория': 'tags',
            }

            labels = ['Издателство', 'Година', 'Език', 'ISBN', 'Категория']
            for label in labels:
                element = soup.find('div', text=label)
                if element:
                    value = element.find_next_sibling('div', class_='prdp__value')
                    if value:
                        key = key_mapping.get(label, label)
                        book_details[key] = value.get_text(strip=True)

            self.__format_book_details(book_details)

        else:
            print(f"{self.__class__.__name__} failed to fetch {item}: {response.status_code}")

    def __get_book_info_multithreaded(self):
        threads = []
        for item in self.individual_search_items:
            thread = threading.Thread(target=self.__get_book_info, args=(item,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def __format_book_details(self, book_details):
        formatted_details = format_book_details(book_details)
        self.formatted_details.append(formatted_details)

    def get_book_list(self):
        return self.formatted_details
