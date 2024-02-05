import pytest
from app.utils.parser import *


def test_func_html_parser_basic():
    html_content = "<html><body><p>This is a <b>sample</b> HTML page</p></body></html>"
    result = html_parser(html_content)
    assert result == "This is a sample HTML page"


def test_func_html_parser_with_css():
    html_content = "<html><head><style>.test { color: red; }</style></head><body><p>This is a <b>sample</b> HTML page</p></body></html>"
    result = html_parser(html_content, include_css=True)
    assert result == "This is a sample HTML page .test { color: red; }"


def test_func_html_parser_with_js():
    html_content = "<html><body><script>alert('Hello');</script><p>This is a <b>sample</b> HTML page</p></body></html>"
    result = html_parser(html_content, include_js=True)
    assert result == "This is a sample HTML page alert('Hello');"


def test_func_html_parser_include_css_false():
    html_content = "<html><head><style>.test { color: red; }</style></head><body><p>This is a <b>sample</b> HTML page</p></body></html>"
    result = html_parser(html_content, include_css=False)
    assert result == "This is a sample HTML page"


def test_func_html_parser_include_js_false():
    html_content = "<html><body><script>alert('Hello');</script><p>This is a <b>sample</b> HTML page</p></body></html>"
    result = html_parser(html_content, include_js=False)
    assert result == "This is a sample HTML page"


def test_func_html_parser_with_exceptions():
    invalid_html_content = (
        "<html><body><p>This is an invalid HTML page<p></body></html>"
    )
    with pytest.raises(Exception, match="HTML Parser:"):
        html_parser(invalid_html_content)
