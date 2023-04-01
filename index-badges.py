import os

import helper

if __name__ == '__main__':
    directory_path = "data/badges"

    files = os.listdir(directory_path)
    print(len(files))
    # Get all the files in the directory
    helper.set_items_from_file(
        helper.get_badges_file("index"),
        files
    )
