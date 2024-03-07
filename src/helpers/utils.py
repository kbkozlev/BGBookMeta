import re
from typing import Dict
import os


def translate_language(language: str) -> str:
    languages = {
        'български': 'Bulgarian'
    }
    return languages.get(language.lower())


def format_book_details(book_details: Dict[str, str]) -> Dict[str, str]:
    """
    Formats the book details dictionary, extracting specific keys and formatting them.

    Args:
    - book_details (Dict[str, str]): Dictionary containing book details.

    Returns:
    - Dict[str, str]: Formatted book details dictionary with specified keys.
    """
    formatted_details = {
        "Book Title": book_details.get("book_title", ""),
        "Author": book_details.get("author", ""),
        "Publisher": book_details.get("publisher", ""),
        "ISBN": book_details.get("ISBN", ""),
        "Language": translate_language(book_details.get("language", "")),
        "Publication Year": book_details.get("publication_year", ""),
        "Cover": book_details.get("img_src", ""),
        "Tags": book_details.get("tags", ""),
        "Description": book_details.get("description", "")
    }
    return formatted_details


def process_title_text(title: str) -> str:
    """
    Processes the input title text, retaining only Cyrillic and Latin alphabets,
    converting the text to lowercase, removing extra spaces, and returning the processed text.

    Args:
    - title (str): The input title text to be processed.

    Returns:
    - str: The processed title text containing only Cyrillic and Latin characters.
    """
    processed_title = re.sub(r'[^a-zA-Zа-яА-Я]+', ' ', title)
    processed_title = re.sub(r'\s+', ' ', processed_title)
    processed_title = processed_title.strip()
    return processed_title.lower()
