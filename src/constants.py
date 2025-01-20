from pathlib import Path


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
DOWNLOADS_DIR = BASE_DIR / 'downloads'


class Choices:
    PRETTY = 'pretty'
    FILE = 'file'


class Dirs:
    DOWNLOADS = 'downloads'
    RESULTS = 'results'


class Texts:
    START_PARSE = 'Парсер запущен'
    FINISH = 'Парсер завершил работу.'
    COMMAND_ARGS = 'Аргументы командной строки: {}'
    FILE_RESULT = 'Файл с результатами был сохранён: {}'
    TAG_NOT_FOUND = 'Не найден тег {} {}'
    RESPONSE_ERROR = 'Ошибка загрузки страницы {}. Подробности: {}'
    PARSER_DESCRIPTION = 'Парсер документации Python'
    PARSER_MODE = 'Режимы работы парсера'
    PARSER_CACHE_CLEAN = 'Очистка кеша'
    PARSER_OUTPUTS = 'Дополнительные способы вывода данных'
    START_ERROR = 'Возникла ошибка при работе программы: {}'
    STATUS_NOT_MATCH = (
        'Несовпадающие статусы: {} Статус в карточке: {} Ожидаемые статусы: {}'
    )
    LOAD_ARCHIVE = 'Архив был загружен и сохранён: {}'


EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
