from pathlib import Path
from utils.paths import PERSONAL_ROOT
from utils.frontmatter_manipulation import get_date, get_frontmatter


def valid_file(file):
    pass


def get_destination(file):
    destination = ""
    data = {}
    post = get_frontmatter(file)
    if post["type"] in [
            "daily", "monthly", "weekly", "quarterly", "yearly"]:
        data["year"], data["month"] = get_date(post)
        data["type"] = post["type"]
        destination = Path(PERSONAL_ROOT) / data["type"].capitalize() / data["year"] / data["month"]
        
    return destination
