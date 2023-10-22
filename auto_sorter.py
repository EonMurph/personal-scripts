import frontmatter
import shutil
from pathlib import Path, PurePath
from scripts_data import OBSIDIAN_ROOT

# Set values
tags = {'study': 'module', 'daily': 'date-created',
        'quarterly': 'year', 'weekly': 'year'}
tag = ''
personal_destination = Path(str(OBSIDIAN_ROOT) + '/I-Personal').absolute()

folders = [path for path in Path(OBSIDIAN_ROOT).glob(
    '[!".", 0]*/**') if Path.is_dir(path)]


def valid(path):  # function for checking if file is from valid folder
    if path.is_dir():
        return False
    # slices path name into parts and checks if any part starts with '.' or '0'
    return all(part[0] not in ".0" for part in path.parts)


files = [path for path in Path(OBSIDIAN_ROOT).rglob(
    "*.md") if valid(path) and frontmatter.check(path)]

# runs through all valid files and sorts them
for file in files:
    if 'type' in frontmatter.load(file).keys():
        note = frontmatter.load(file)
        if note['type'] in tags:
            tag = tags[note['type']]
        # sets default location if doesn't match any if statements
        destination = Path(OBSIDIAN_ROOT) / 'Unsorted'
    else:
        continue

    if tag in ['date-created', 'year']:  # checks if file is a daily/quarterly/weekly entry
        year = month = ''
        year = note[tag].split('-')[0]  # grabs the year from the frontmatter
        if tag == 'date-created':
            # grabs the month from the frontmatter
            month = note[tag].split('-')[1]
            destination = personal_destination / 'Daily' / \
                year / month  # if month value then daily entry
        else:
            # if not then sort based on titled type metadata
            destination = personal_destination / note['type'].title() / year

    elif tag == 'module':
        for folder in folders:
            split_folder = PurePath(folder).name.split(
                '_')  # split final folder in path
            if split_folder[0] == note[tag]:
                destination = folder.absolute()  # sets destination based on module code

    elif note[tag] in ['weekly', 'monthly', 'yearly']:  # sorts all other periodic entries
        destination = personal_destination / note[tag].title()

    if not destination in folders:
        Path(destination).mkdir(parents=True, exist_ok=True)

    if Path(file).parent.absolute() != destination:
        shutil.move(file, (destination))  # moves files if not already sorted

    if destination == Path(OBSIDIAN_ROOT) / 'Unsorted':
        print(f'!!{file} has not been sorted!!')
