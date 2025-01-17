from collections import Counter
import csv
import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        # Если основная страница не загрузится, программа закончит работу.
        return
    soup = BeautifulSoup(response.text, features='lxml')

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = main_div.find('div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')

    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = main_tag.find('table', {'class': 'docutils'})
    pdf_a4_tag = table_tag.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)

    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, features='lxml')
    main_block = find_tag(soup, 'section', attrs={'id': 'index-by-category'})
    sections = main_block.find_all('section')
    table_statuses = []
    article_statuses_links = []
    article_statuses = []
    pep_links = []
    for section in sections:
        rows = section.table.tbody.find_all('tr')
        for row in rows:
            # Получить статусы из таблиц
            tds = row.find_all('td')
            table_info = tds[0].abbr.get('title').split(", ")
            pep_links.append(tds[1].a.get('href'))
            if len(table_info) == 2:
                table_statuses.append(table_info[1])
            else:
                table_statuses.append(None)

            # Получить статусы со страницы каждого PEP'а
            full_url = PEP_URL + tds[1].a.get('href')
            pep_response = get_response(session, full_url)
            pep_soup = BeautifulSoup(pep_response.text, features='lxml')
            article_head = find_tag(
                pep_soup,
                'section',
                attrs={'id': 'pep-page-section'}).article.section.dl
            status_dt = None
            for dt in article_head.find_all('dt'):
                if 'Status' in dt.get_text(strip=True):
                    status_dt = dt
                    break
            status_dd = status_dt.find_next_sibling('dd')
            result_status = status_dd.find('abbr').get_text()
            article_statuses_links.append([full_url, result_status])
            article_statuses.append(result_status)

    for i in range(len(article_statuses_links)):
        if (table_statuses[i] is not None and table_statuses[i] !=
                article_statuses_links[i][1]):
            logging.info('Несовпадающие статусы:'
                         f'{article_statuses_links[i][0]}'
                         f'Статсус в карточке: {article_statuses_links[i][1]}'
                         f'Ожидаемые статусы: {table_statuses[i]}')

    counts = Counter(article_statuses)
    total_count = sum(counts.values())

    filename = 'statuses_summary.csv'
    downloads_dir = BASE_DIR / 'results'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    with open(archive_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Статус", "Количество"])
        for status, count in counts.items():
            writer.writerow([status, count])
        writer.writerow(["Total", total_count])


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
