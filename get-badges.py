import helper

if __name__ == '__main__':
    organizations = helper.get_items_from_file(helper.get_organizations_file())
    for organization in organizations.values():
        print(organization['name'])

        badges = helper.get_items_from_file(helper.get_badges_file(organization['id']))
        if not len(badges) == 0:
            print("Badges found skipping")
            continue

        badges = helper.get_badges(badges, "https://www.credly.com" + organization['url'] + ".json")

        helper.set_items_from_file(helper.get_badges_file(organization['id']), badges)
