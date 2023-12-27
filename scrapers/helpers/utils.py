import re
import string
from .language_dict import languages


def translate_language(language):
    return languages.get(language.lower())


def format_book_details(book_details):
    formatted_details = {
        "book_title": book_details.get("book_title", ""),
        "author": book_details.get("author", ""),
        "publisher": book_details.get("publisher", ""),
        "ISBN": book_details.get("ISBN", ""),
        "language": translate_language(book_details.get("language", "")),
        "publication_year": book_details.get("publication_year", ""),
        "img_src": book_details.get("img_src", ""),
        "tags": book_details.get("tags", ""),
        "description": book_details.get("description", "")
    }
    return formatted_details


def process_title_text(title):
    punctuation = re.escape(string.punctuation)
    processed_title = re.sub(r'[{}]+'.format(punctuation), '', title)
    processed_title = re.sub(r'\s+', ' ', processed_title)
    processed_title = processed_title.strip()
    return processed_title.lower()

