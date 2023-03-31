import json
import os

import requests


def get_skills_file():
    return 'data/skills.json'


def get_organizations_file():
    return 'data/organizations.json'


def get_badges_file():
    return 'data/badges.json'


def get_search_terms_file():
    return 'data/search-terms.json'


def get_items_by_search_term(search_term):
    r = requests.get('https://www.credly.com/api/v1/global_search?q=' + search_term)
    return r.json()['data']


def search_terms():
    with open(get_search_terms_file(), 'r') as file:
        return json.load(file)


def get_items_from_file(file_name):
    if os.path.isfile(file_name):
        # read json data from file
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        # create a dictionary if file does not exist
        return {}


def set_items_from_file(file_name, items):
    with open(file_name, "w") as outfile:
        json.dump(items, outfile)


def crawl_search_terms(terms):
    organizations = get_items_from_file(get_organizations_file())
    skills = get_items_from_file(get_skills_file())

    for search_term in terms:
        items = get_items_by_search_term(search_term)
        print(search_term, len(items))
        for item in items:
            if item['type'] == 'Organization':
                item['logo'] = item['photo']['url']
                del item["type"]
                del item["photo"]

                organizations[item['id']] = item
            elif item['type'] == 'Skill':
                skills[item['id']] = item
    set_items_from_file(get_organizations_file(), organizations)
    set_items_from_file(get_skills_file(), skills)
