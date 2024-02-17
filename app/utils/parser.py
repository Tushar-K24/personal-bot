import re

from bs4 import BeautifulSoup


def html_parser(html_page: str) -> str:
    """
    Removes tags from HTML page and returns the raw text (word soup) as string

    :param html_page(str): html page as a string

    :return (str): html page with removed tags
    """
    try:
        soup: BeautifulSoup = BeautifulSoup(html_page, "html.parser")
        # check if page is valid
        if html_page != str(soup):
            raise Exception(f"Invalid HTML Page")

        # Extract text content from the HTML
        text_content = soup.get_text(separator=" ", strip=True)

        # Remove extra whitespaces
        text_content = re.sub("\s+", " ", text_content).strip()

        return text_content
    except Exception as err:
        raise Exception(f"HTML Parser --> {err}")
