import frontmatter
import shutil
from utils import get_frontmatter, PERSONAL_ROOT, valid_file, get_date, get_destination
from pathlib import Path, PurePath

files = [path
         for path in Path(PERSONAL_ROOT).rglob("*.md") 
         if frontmatter.check(path)]

for file in files:
    post = get_frontmatter(file)
    if all(key in post.keys() for key in ["type", "date-created"]):
        destination = get_destination(file)
        if Path(file).parent != destination:
            shutil.move(file, destination)
