
# 📚 Python Documentation Parser  

This project includes several **parsers for Python documentation**, managed via a command-line interface.  

- 🖥️ Convenient menu with different parser modes.  
- 🗑 Ability to clear cached HTML pages.  
- 📝 Built-in logger (output to terminal or to a separate file).  

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone git@github.com:VilmenAbramian/bs4_parser_pep.git
```
2. Navigate to the project folder and create a virtual environment:
```bash
cd bs4_parser_pep
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Run the console menu from the src folder:
```bash
python main.py --help
```

## ⚙️ Parser Modes
```bash
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Python documentation parser

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Parser modes

options:
  -h, --help            Show this help message and exit
  -c, --clear-cache     Clear the cache
  -o {pretty,file}, --output {pretty,file}
                        Additional output options
```

## 📰 whats-new
Collects data from https://docs.python.org/3/ and outputs links to articles about new features in each Python release, including the article title and the editors.

**Example output:**
```
https://docs.python.org/3/whatsnew/3.13.html What’s New In Python 3.13¶  Editors: Adam Turner and Thomas Wouters  
https://docs.python.org/3/whatsnew/3.12.html What’s New In Python 3.12¶  Editor: Adam Turner  
https://docs.python.org/3/whatsnew/3.11.html What’s New In Python 3.11¶  Editor: Pablo Galindo Salgado  
https://docs.python.org/3/whatsnew/3.10.html What’s New In Python 3.10¶  Editor: Pablo Galindo Salgado  
https://docs.python.org/3/whatsnew/3.9.html What’s New In Python 3.9¶  Editor: Łukasz Langa  
https://docs.python.org/3/whatsnew/3.8.html What’s New In Python 3.8¶  Editor: Raymond Hettinger
```
## 📌 latest-versions
Outputs information about all Python versions and their statuses.

**Example output:**
```
https://docs.python.org/3.14/ 3.14 in development
https://docs.python.org/3.13/ 3.13 stable
https://docs.python.org/3.12/ 3.12 stable
https://docs.python.org/3.11/ 3.11 security-fixes
https://docs.python.org/3.10/ 3.10 security-fixes
https://docs.python.org/3.9/ 3.9 security-fixes
https://docs.python.org/3.8/ 3.8 EOL
```
## 📥 download
Downloads the Python documentation archive to the local downloads folder.

## 📊pep
Creates a .csv file in the results folder containing a table with two columns: the PEP document status type and the number of documents with that status. The information is collected from: https://peps.python.org/pep-0000/.

**Example output:**
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

## 🛠 Technologies Used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-green?style=for-the-badge)

## 👤 Author
[Vilmen Abramian](https://github.com/VilmenAbramian), vilmen.abramian@gmail.com

Sprint 19
