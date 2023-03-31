import requests

import helper


def get_badges(badges, url):
    r = requests.get(url).json()
    for badge in r["data"]:
        badges[badge['id']] = badge
    if r["metadata"]["next_page_url"]:
        get_badges(badges, r["metadata"]["next_page_url"])
    return badges


if __name__ == '__main__':
    organizations = helper.get_items_from_file(helper.get_organizations_file())
    for organization in organizations.values():
        badges = helper.get_items_from_file(helper.get_badges_file())

        organization["name"] = "amazon-web-services"
        organization["url"] = "organizations/amazon-web-services/badges"
        # [None, 'Paid', 'Free']

        badges = get_badges(badges, "https://www.credly.com/" + organization['url'] + ".json")

        helper.set_items_from_file(helper.get_badges_file(), badges)
        exit()

        # print(organization['name'])
        # r = requests.get("https://www.credly.com/" + organization['url'] + ".json").json()
        # # print(r["data"])
        # for badge in r["data"]:
        #     costs.append(badge.get("cost")) if badge.get("cost") not in costs else costs
        #
        # if r["metadata"]["next_page_url"]:
        #     r = requests.get(r["metadata"]["next_page_url"]).json()
        #     for badge in r["data"]:
        #         costs.append(badge.get("cost")) if badge.get("cost") not in costs else costs
        # print(costs)