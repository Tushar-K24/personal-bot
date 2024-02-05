from bs4 import BeautifulSoup
import re


def html_parser(
    html_page: str, include_css: bool = False, include_js: bool = False
) -> str:
    """
    Removes tags from HTML page and returns the raw text (word soup) as string

    :param html_page(str): html page as a string
    :param include_css(bool): whether to include css in word soup
    :param include_js(bool): whether to include javascript in word soup

    :return (str): html page with removed tags
    """
    try:
        soup = BeautifulSoup(html_page, "html.parser")

        # Remove script and style tags if include_js or include_css is False
        if not include_js:
            for script in soup(["script", "noscript"]):
                script.decompose()

        if not include_css:
            for style in soup(["style"]):
                style.decompose()

        # Extract text content from the HTML
        text_content = soup.get_text(separator=" ", strip=True)

        # Remove extra whitespaces
        text_content = re.sub("\s+", " ", text_content).strip()

        return text_content
    except Exception as err:
        raise Exception(f"HTML Parser: {err}")
