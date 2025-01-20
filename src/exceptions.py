class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class NotFoundError(Exception):
    """Вызывается, когда ожидаемый элемент не найден на странице."""
