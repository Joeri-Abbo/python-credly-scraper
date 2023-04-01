import sys

import helper

if __name__ == '__main__':
    sys.argv[1]
    organizations = helper.get_items_from_file(helper.get_organizations_file())
    for organization in organizations.values():
        if sys.argv[1] == organization['id']:
            badges = helper.get_items_from_file(helper.get_badges_file(organization['id']))
            badges = helper.get_badges(badges, "https://www.credly.com" + organization['url'] + ".json")

            helper.set_items_from_file(helper.get_badges_file(organization['id']), badges)
            print("Done")
            exit()
    print("Not found")
