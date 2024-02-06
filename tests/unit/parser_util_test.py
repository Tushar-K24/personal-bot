import pytest

from app.utils.parser import *


def test_func_html_parser():
    html_content = "<html><body><p>This is a <b>sample</b> HTML page</p></body></html>"
    result = html_parser(html_content)
    assert result == "This is a sample HTML page"


def test_func_html_parser_with_exceptions():
    invalid_html_content = (
        "<html><body><p>This is an invalid HTML page<p></body></html>"
    )
    with pytest.raises(Exception, match="HTML Parser:"):
        html_parser(invalid_html_content)
