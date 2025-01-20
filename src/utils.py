from bs4 import BeautifulSoup
from requests import RequestException

from constants import Texts
from exceptions import ParserFindTagException


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(
            Texts.RESPONSE_ERROR.format(url, error)
        )


# Перехват ошибки поиска тегов.
def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(Texts.TAG_NOT_FOUND.format(tag, attrs))
    return searched_tag


def calculate_soup(session, url):
    response = get_response(session, url)
    if response is None:
        return None
    return BeautifulSoup(response.text, features='lxml')
