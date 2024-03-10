import cloudscraper
from requests_html import AsyncHTMLSession
from src.helpers.utils import format_book_details, process_title_text
import asyncio


class OrangeScraper:
    def __init__(self, search_term):
        self.formatted_details = []
        self.individual_search_items = set()

        scraper = cloudscraper.create_scraper()

        url = f"https://www.orangecenter.bg/catalogsearch/result/?q={search_term}"
        response = scraper.get(url)

        if response.status_code == 200:
            loop = asyncio.get_event_loop()
            self.session = AsyncHTMLSession()
            loop.run_until_complete(self.__process_response(url, search_term))
        else:
            print(f"{self.__class__.__name__} failed to fetch the main page: {response.status_code}")

    async def __process_response(self, url, search_term):
        session_response = await self.session.get(url)
        await session_response.html.arender()
        await self.__extract_individual_search_items(session_response.html, search_term)

        # Gather book info concurrently
        await asyncio.gather(*[self.__get_book_info(item) for item in self.individual_search_items])

    async def __extract_individual_search_items(self, html, search_term):
        product_items = html.find('a.product-item-info')

        for item in product_items:
            title = item.find('strong.product-item-name', first=True).text.strip()
            processed_title = process_title_text(title)
            search = process_title_text(search_term)

            if search in processed_title:
                href = item.attrs['href']
                self.individual_search_items.add(href)

    async def __get_book_info(self, item):
        response = await self.session.get(item)

        if response.status_code == 200:
            await response.html.arender()
            book_details = {
                "book_title": response.html.find('span.base[data-ui-id="page-title-wrapper"]', first=True).text,
                "img_src": response.html.find("img.fotorama__img", first=True).attrs['src'],
                "description": ' '.join(paragraph.text.strip() for paragraph in
                                        response.html.find('div.description div.text p'))
            }

            key_mapping = {
                'Автор': 'author',
                'Издателство': 'publisher',
                'Език': 'language',
                'Година на издаване': 'publication_year',
                'ISBN': 'ISBN'
            }

            ul_elements = response.html.find('ul.attributes__list')

            for ul in ul_elements:
                li_elements = ul.find('li.attributes__item')
                for li in li_elements:
                    key_element = li.find('span.attributes__item-title', first=True)
                    value_element = li.find('span.attributes__item-info', first=True)
                    if key_element and value_element:
                        key = key_element.text.strip()
                        if key in key_mapping:
                            value = value_element.text.strip()
                            book_details[key_mapping[key]] = value

            self.__format_book_details(book_details)

        else:
            print(f"{self.__class__.__name__} failed to fetch {item}: {response.status_code}")

    def __format_book_details(self, book_details):
        formatted_details = format_book_details(book_details)
        self.formatted_details.append(formatted_details)

    def get_book_list(self):
        return self.formatted_details
