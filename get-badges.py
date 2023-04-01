import helper
import multiprocessing


def process_organization(organization):
    print(organization['name'])

    badges = helper.get_items_from_file(helper.get_badges_file(organization['id']))
    if not len(badges) == 0:
        print("Badges found skipping")
        return

    badges = helper.get_badges(badges, "https://www.credly.com" + organization['url'] + ".json")

    helper.set_items_from_file(helper.get_badges_file(organization['id']), badges)


if __name__ == '__main__':
    organizations = helper.get_items_from_file(helper.get_organizations_file())
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_organization, organizations.values())
