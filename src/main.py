from collections import Counter
import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, PEP_URL, Dirs, Texts
from exceptions import NotFoundError
from outputs import control_output
from utils import calculate_soup, find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = calculate_soup(session, whats_new_url)
    version_a_tag = soup.select(
            '#what-s-new-in-python div.toctree-wrapper'
            ' li.toctree-l1 a[href$=".html"]'
        )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    errors = []
    for link in tqdm(version_a_tag):
        version_link = urljoin(whats_new_url, link['href'])
        try:
            soup = calculate_soup(session, version_link)
            results.append(
                (
                    version_link,
                    find_tag(soup, 'h1').text,
                    find_tag(soup, 'dl').text.replace('\n', ' ')
                )
            )
        except ConnectionError as e:
            errors.append(Texts.RESPONSE_ERROR.format(version_link, e))
    [*map(logging.error, errors)]
    return results


def latest_versions(session):
    soup = calculate_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise NotFoundError(Texts.NOTHING_FOUND)

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = calculate_soup(session, downloads_url)

    main_tag = find_tag(soup, 'div', {'role': 'main'})
    pdf_a4_link = main_tag.select_one(
        'table.docutils a[href$="pdf-a4.zip"]'
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)

    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / Dirs.DOWNLOADS
    downloads_dir.mkdir(parents=True, exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(Texts.LOAD_ARCHIVE.format(archive_path))


def pep(session):
    soup = calculate_soup(session, PEP_URL)
    main_block = find_tag(soup, 'section', attrs={'id': 'index-by-category'})
    sections = main_block.find_all('section')
    table_statuses = []
    article_statuses_links = []
    article_statuses = []
    pep_links = []
    errors = []
    for section in sections:
        rows = section.table.tbody.find_all('tr')
        for row in rows:
            # Получить статусы из таблиц
            tds = row.find_all('td')
            table_info = tds[0].abbr.get('title').split(', ')
            pep_links.append(tds[1].a.get('href'))
            if len(table_info) == 2:
                table_statuses.append(table_info[1])
            else:
                table_statuses.append(None)

            try:
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
            except ConnectionError as e:
                errors.append(Texts.RESPONSE_ERROR.format(full_url, e))
        [*map(logging.error, errors)]

    for i in range(len(article_statuses_links)):
        if (table_statuses[i] is not None and table_statuses[i] !=
                article_statuses_links[i][1]):
            logging.info(
                Texts.STATUS_NOT_MATCH.format(
                    article_statuses_links[i][0],
                    article_statuses_links[i][1],
                    table_statuses[i]
                )
            )

    counts = Counter(article_statuses)

    return [
        ('Статус', 'Количество'),
        *counts.items(),
        ('Всего', sum(counts.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info(Texts.START_PARSE)

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(Texts.COMMAND_ARGS.format(args))

    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as e:
        logging.error(Texts.START_ERROR.format(e))
    logging.info(Texts.FINISH)


if __name__ == '__main__':
    main()
