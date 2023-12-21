from bs4 import BeautifulSoup
import cloudscraper


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
            self.extract_individual_search_items(html_content)
            self.combine_get_and_extract_book_info()
        else:
            print("Failed to fetch the page:", response.status_code)

    def extract_individual_search_items(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        my_divs = soup.select("div.col-sm-4.col-md-3.col-xs-6 a[href^='/']:not([href^='/#'])")

        for a_tag in my_divs:
            href = a_tag.get('href')
            if href:
                self.individual_search_items.add(href)

    def combine_get_and_extract_book_info(self):
        for item in self.individual_search_items:
            url = f"https://g.helikon.bg{item}"
            response = self.scraper.get(url)

            if response.status_code == 200:
                html_content = response.content
                self.extract_book_info(html_content)
            else:
                print("Failed to fetch the page:", response.status_code)

    def extract_book_info(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extracting book title, author, and image source
        book_title = soup.find(class_='_box-highlight').find('h3').text.strip()
        author = soup.find(class_='_box-highlight').find('h5').text.strip('Автор: ')
        image_source = soup.find(class_='popup-gallery-image').find('img')['src']
        tab_content_div = soup.find('div', class_='tab-pane fade in active', id='annotation')

        text_inside_div = tab_content_div.get_text(separator='\n', strip=True)

        # Extracting other book details from tables
        book_details = {
            "Book Title": book_title,
            "Author": author,
            "Image Source": image_source,
        }

        html_data = soup.find_all('table')
        for html_table in html_data:
            table_rows = html_table.find_all('tr')

            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    # Mapping dictionary for key renaming
                    key_mapping = {
                        'Издател': 'Publisher',
                        'Език': 'Language',
                        'Година на издаване': 'Publishing Date',
                        'ISBN': 'ISBN',
                        'Категории': 'Tags',
                    }
                    if key in key_mapping:
                        book_details[key_mapping[key]] = value

        # Adding Annotation key at the end
        book_details["Annotation"] = text_inside_div

        print(book_details)
