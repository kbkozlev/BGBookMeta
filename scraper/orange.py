from bs4 import BeautifulSoup
import cloudscraper
import re


class OrangeScraper:
    def __init__(self, search_term):
        self.individual_search_items = set()
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False}
        )
        url = f"https://www.orangecenter.bg/catalogsearch/result/index/?cat=2204&q={search_term}"
        response = self.scraper.get(url)

        if response.status_code == 200:
            html_content = response.content
            self.extract_individual_search_items(html_content, search_term)
            self.get_book_info()
        else:
            print("Failed to fetch the page:", response.status_code)

    def extract_individual_search_items(self, html_content, search_term):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_items = soup.find_all('a', class_='product-item-info')

        for item in product_items:
            title = item.find('strong', class_='product-item-name').text.strip()
            processed_title = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', title)).strip()

            if search_term.lower() in processed_title.lower():
                href = item['href']
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
        book_details = {
            "book_title": soup.find('span', {'class': 'base', 'data-ui-id': 'page-title-wrapper'}).get_text(),
            "author": "", "img_src": "", "publisher": "", "language": "", "publication_year": "", "ISBN": "",
            "tags": "", "description": ""}

        og_image_meta = soup.find("meta", property="og:image")
        if og_image_meta:
            book_details["img_src"] = og_image_meta["content"]

        description_div = soup.find('div', class_='description')
        if description_div:
            text_div = description_div.find('div', class_='text')
            if text_div:
                description_text = ' '.join(paragraph.text.strip() for paragraph in text_div.find_all('p'))
                book_details["description"] = description_text

        specific_elements = {
            'Автор': 'author',
            'Издателство': 'publisher',
            'Език': 'language',
            'Година на издаване': 'publication_year',
            'ISBN': 'ISBN'
        }

        ul_elements = soup.find_all('ul', class_='attributes__list')

        for ul in ul_elements:
            li_elements = ul.find_all('li', class_='attributes__item')
            for li in li_elements:
                key_element = li.find('span', class_='attributes__item-title')
                value_element = li.find('span', class_='attributes__item-info')
                if key_element and value_element:
                    key = key_element.get_text(strip=True)
                    if key in specific_elements:
                        value = value_element.get_text(strip=True)
                        book_details[specific_elements[key]] = value

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
