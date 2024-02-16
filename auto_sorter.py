import shutil
from utils import get_frontmatter, get_destination, get_files
from pathlib import Path, PurePath


if __name__ == "__main__":
    for file in get_files():
        post = get_frontmatter(file)
        if all(key in post.keys() for key in ["type", "date-created"]):
            destination = get_destination(file)
            if Path(file).parent != destination:
                shutil.move(file, destination)
