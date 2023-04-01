import requests

import helper


def get_badges(badges, url):
    print(url)
    try:
        r = requests.get(url).json()
        for badge in r["data"]:
            badges[badge['id']] = badge
        if r["metadata"]["next_page_url"]:
            get_badges(badges, r["metadata"]["next_page_url"])
    except:
        print("Error")
    return badges


if __name__ == '__main__':
    skip = True
    organizations = helper.get_items_from_file(helper.get_organizations_file())
    for organization in organizations.values():
        print(organization['name'])
        if organization['name'] == "ERICSSON":
            skip = False

        if not skip:
            badges = helper.get_items_from_file(helper.get_badges_file())

            # [None, 'Paid', 'Free']

            badges = get_badges(badges, "https://www.credly.com/" + organization['url'] + ".json")

            helper.set_items_from_file(helper.get_badges_file(), badges)
        else:
            print("skip")
