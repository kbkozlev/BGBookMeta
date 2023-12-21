from bs4 import BeautifulSoup
import cloudscraper


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
            self.extract_individual_search_items(html_content)
            self.get_book_info()
        else:
            print("Failed to fetch the page:", response.status_code)

    def extract_individual_search_items(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_links = soup.select('.products.wrapper .product-item-info')

        for link in product_links:
            href = link['href']
            if href:
                self.individual_search_items.add(href)

    def get_book_info(self):
        for item in self.individual_search_items:
            response = self.scraper.get(item)

            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')

                book_title = soup.find('span', {'class': 'base', 'data-ui-id': 'page-title-wrapper'}).get_text()
                og_image_meta = soup.find("meta", property="og:image")
                image_url = og_image_meta["content"]
                description_div = soup.find('div', class_='description').find('div', class_='text').find_all('p')
                combined_text = ' '.join(paragraph.text.strip() for paragraph in description_div)

                book_details = {
                    "Book Title": book_title,
                    "Author": "",  # Placeholder for Author (will be updated later)
                    "Image Source": image_url,
                    "Publisher": "",  # Placeholder for Publisher (will be updated later)
                    "Language": "",  # Placeholder for Language (will be updated later)
                    "Publication Year": "",  # Placeholder for Publication Year (will be updated later)
                    "ISBN": "",  # Placeholder for ISBN (will be updated later)
                    "Description": combined_text
                }

                # Find specific elements and extract their values
                specific_elements = {
                    'Автор': 'Author',
                    'Издателство': 'Publisher',
                    'Език': 'Language',
                    'Година на издаване': 'Publication Year',
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
                                # Update the corresponding placeholders in book_details
                                book_details[specific_elements[key]] = value

                # Rearrange the book_details dictionary in the desired order
                reordered_book_details = {
                    "book_title": book_details["Book Title"],
                    "author": book_details["Author"],
                    "img_src": book_details["Image Source"],
                    "publisher": book_details["Publisher"],
                    "language": book_details["Language"],
                    "publication_year": book_details["Publication Year"],
                    "ISBN": book_details["ISBN"],
                    "description": book_details["Description"]
                }

                print(reordered_book_details)

            else:
                print("Failed to fetch the page:", response.status_code)
