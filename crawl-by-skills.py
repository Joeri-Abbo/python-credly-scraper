import helper

if __name__ == '__main__':
    skills = []
    for skill in helper.get_items_from_file(helper.get_skills_file()).values():
        skills.append(skill['name'])
    helper.crawl_search_terms(skills)
