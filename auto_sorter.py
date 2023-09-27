import frontmatter, shutil, re
from pathlib import Path, PurePath

# Set values
tags = {'study': 'module', 'daily': 'date-created', 'quarterly': 'year', 'weekly': 'year'}
tag = ''
wd = Path('E:/Obsidian/Brain_Cell_Storage/').absolute()
personal_destination = Path(str(wd) + '/I-Personal').absolute()

folders = [path for path in Path(wd).glob('[!".", 0]*/**') if Path.is_dir(path)]


def valid(path): # function for checking if file is from valid folder
    if path.is_dir(): return False
    return all(part[0] not in ".0" for part in path.parts) # slices path name into parts and checks if any part starts with '.' or '0'


files = [path for path in Path(wd).rglob("*.md") if valid(path) and frontmatter.check(path)]

# runs through all valid files and sorts them
for file in files:
    if 'type' in frontmatter.load(file).keys():
        note = frontmatter.load(file)
        if note['type'] in tags: tag = tags[note['type']]
        destination = Path(wd) / 'Unsorted' # sets default location if doesn't match any if statements
    else: continue

    if tag in ['date-created', 'year']: # checks if file is a daily/quarterly/weekly entry
        year = month = ''
        year = note[tag].split('-')[0] # grabs the year from the frontmatter
        if tag == 'date-created': month = re.split('[-_]', note[tag])[1] # grabs the month from the frontmatter
        if month != '': destination = personal_destination / 'Daily' / year / month # if month value then daily entry
        else: destination = personal_destination / note['type'].title() / year # if not then sort based on titled type metadata

    elif tag == 'module': 
        for folder in folders:
            split_folder = re.split('_', PurePath(folder).name) # split final folder in path
            if split_folder[0] == note[tag]: destination = folder.absolute() # sets destination based on module code
            
    elif note[tag] in ['weekly', 'monthly', 'yearly']: # sorts all other periodic entries
        destination = personal_destination / note[tag].title()

    if Path(file).parent.absolute() != destination: shutil.move(file, destination) # moves files if not already sorted
