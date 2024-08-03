import yaml
import argparse
import subprocess
from datetime import date
from pathlib import Path
from utils import PERSONAL_ROOT, get_destination, get_files

# creates arguments for command line
parser = argparse.ArgumentParser(
    description="creates a markdown file based on yaml file")
parser.add_argument("file", type=str, help="enter the yaml file")
args = parser.parse_args()


yaml_file_location = f"templates/{args.file}.yaml"
with open(yaml_file_location, "r") as yaml_file:
    template = yaml.full_load(yaml_file)

    md_frontmatter = template.get("frontmatter", None)
    if "date-created" in md_frontmatter:
        exec(md_frontmatter["date-created"])


def date_suffix():  # decides on date suffix for h1 based on last digit in day date
    if (digit := date.today().strftime("%d")[-1]) in (prefix := {"1":"st", "2":"nd", "3":"rd"}):
        return prefix[digit]
    else:
        return "th"


markdown = template["markdown"].replace("DATE-PLACEHOLDER", date.today().strftime(
    f"%B %d{date_suffix()}, %Y"))  # replaces "date-created" code with result

# sets default file name
md_file = "Untitled.md"

if "title" in template:
    exec(template["title"])

if (md_file) not in (files:=[str(path.name) for path in Path(PERSONAL_ROOT).glob("**/*") if path.is_file()]):
    with open(PERSONAL_ROOT + md_file, "w") as file:
        # writes frontmatter for md file
        file.write("---\n")
        for key in md_frontmatter:
            file.write(f"{key}: {md_frontmatter[key]}\n")
        file.write("---\n\n")

        file.write(markdown)  # writes markdown template

subprocess.run(["python", "auto_sorter.py"])

for file in get_files():
    if str(file.name).replace(".md", "") == date.today().strftime("%Y-%b-%d"):
        destination = get_destination(file)
        break
subprocess.run(["code.cmd", destination], shell=True)
subprocess.run(["code.cmd", destination / md_file], shell=True)
