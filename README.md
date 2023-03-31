# Project: Credly Crawler (WIP)

This project consists of Python scripts designed to crawl and extract data from the Credly platform. The main components
of the project are:

1. crawl-by-arg.py
2. crawl-by-search-terms.py
3. crawl-by-skills.py
4. get-badges.py
5. helper.py

## Requirements

Python 3.x
requests library
Install the requirements using the following command:

```bash
pip install requests 
```

## Usage

### 1. crawl-by-arg.py

This script crawls the Credly platform using a single search term passed as a command-line argument.

Usage:

```bash
python crawl-by-arg.py <search_term>
```

### 2. crawl-by-search-terms.py

This script crawls the Credly platform using a list of search terms specified in the `data/search-terms.json` file.

#### Usage:

```bash
python crawl-by-search-terms.py
```

### 3. crawl-by-skills.py

This script crawls the Credly platform using a list of skills that are retrieved from the data/skills.json file.

#### Usage:

```bash
python crawl-by-skills.py
```

### 4. get-badges.py

This script retrieves all badges for each organization specified in the data/organizations.json file. The badges are
then saved to the data/badges.json file.

#### Usage:

```bash
python get-badges.py
```

### 5. helper.py

This script contains helper functions used by the other scripts in this project. Functions include:

- get_skills_file()
- get_organizations_file()
- get_badges_file()
- get_search_terms_file()
- get_items_by_search_term(search_term)
- search_terms()
- get_items_from_file(file_name)
- set_items_from_file(file_name, items)
- crawl_search_terms(terms)

## Notes

Before running the scripts, make sure to create the necessary data files in the data directory:

- skills.json
- organizations.json
- badges.json
- search-terms.json

Each of these files should contain an empty JSON object {} if there is no initial data.