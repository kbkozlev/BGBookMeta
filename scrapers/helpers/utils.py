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