# Парсер документации Python
[Абрамян Вильмен Левонович](vilmen.abramian@gmail.com)

Проект включает в себя несколько парсеров для материалов, связанных с документацией Python. Для удобства работы с программой предусмотрен консольный интерфейс, позволяющий выбрать тот или иной парсер, а также удалить закешированные html-страницы сайтов. Также предусмотрен логгер, который может выводить данные в терминал или в отдельный файл в зависимости от выбора пользователя. Выбрать режим работы логгера можно также через консольный интерфейс.

## Для установки и запуска программы нужно
Склонировать репозиторий:
```
git clone git@github.com:VilmenAbramian/bs4_parser_pep.git
```
Перейти в папку проекта, создать и активировать виртуальное окружение:
```
cd bs4_parser_pep
python -m venv venv
source venv/bin/activate #(для Linux, MacOS)
venv\Scripts\activate #(для Windows)
```
Установить необходимые зависимости:
```
pip install -r requirements.txt
```
Перейти в папку src и выполнить команду:
```
python main.py --help
```
Тогда будет отображено консольное меню:
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

options:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных

```
Для запуска программы в режиме pep:
```
python main.py pep
```

## whats-new
Собирает данные с сайта https://docs.python.org/3/ и выводит ссылки на статьи, содержащие информацию о нововведениях очередной версии Python, название соответствующей статьи, а также авторов. Пример вывода:
```
https://docs.python.org/3/whatsnew/3.13.html What’s New In Python 3.13¶  Editors: Adam Turner and Thomas Wouters  
https://docs.python.org/3/whatsnew/3.12.html What’s New In Python 3.12¶  Editor: Adam Turner  
https://docs.python.org/3/whatsnew/3.11.html What’s New In Python 3.11¶  Editor: Pablo Galindo Salgado  
https://docs.python.org/3/whatsnew/3.10.html What’s New In Python 3.10¶  Editor: Pablo Galindo Salgado  
https://docs.python.org/3/whatsnew/3.9.html What’s New In Python 3.9¶  Editor: Łukasz Langa  
https://docs.python.org/3/whatsnew/3.8.html What’s New In Python 3.8¶  Editor: Raymond Hettinger
```
## latest-versions
Выводит информацию о всех версиях Python и их статусах. Пример вывода:
```
https://docs.python.org/3.14/ 3.14 in development
https://docs.python.org/3.13/ 3.13 stable
https://docs.python.org/3.12/ 3.12 stable
https://docs.python.org/3.11/ 3.11 security-fixes
https://docs.python.org/3.10/ 3.10 security-fixes
https://docs.python.org/3.9/ 3.9 security-fixes
https://docs.python.org/3.8/ 3.8 EOL
```
## download
Скачивает архив с документацией Python на локальный диск в папку downloads

## pep
Записывает в папку results .csv файл, содержащий таблицу с двумя столбцами:  тип статуса документа pep и количество документов pep, соответствующих этому статусу. Используется информация с сайта: https://peps.python.org/pep-0000/. Пример информации, записанной в файл:
```
Статус,Количество  
Active,34  
Final,328  
Accepted,18  
Provisional,2  
Draft,40  
Superseded,24  
Deferred,35  
Withdrawn,65  
Rejected,123  
April Fool!,1  
Total,670
```

Спринт 19