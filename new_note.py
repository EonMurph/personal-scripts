import yaml
import argparse
import subprocess
from datetime import date
from pathlib import Path
from scripts_data import *

# creates arguments for command line
parser = argparse.ArgumentParser(
    description='creates a markdown file based on yaml file')
parser.add_argument('file', type=str, help='enter the yaml file')
args = parser.parse_args()

with open(args.file, 'r') as yaml_file:
    template = yaml.full_load(yaml_file)

    md_frontmatter = template.get('frontmatter', None)
    if 'date-created' in md_frontmatter:
        exec(md_frontmatter['date-created'])


def date_suffix():  # decides on date suffix for h1 based on last digit in day date
    if (digit := date.today().strftime('%d')[-1]) in ['1', '2', '3']:
        if digit == '1':
            return 'st'
        elif digit == '2':
            return 'nd'
        else:
            return 'rd'
    else:
        return 'th'


markdown = template['markdown'].replace('DATE-PLACEHOLDER', date.today().strftime(
    f'%B %d{date_suffix()}, %Y'))  # replaces 'date-created' code with result

# sets default file name
md_file = 'Untitled.md'

if 'title' in template:
    exec(template['title'])

if (md_file) not in [str(path.name) for path in Path(OBSIDIAN_ROOT).glob('**/*')]:
    with open(OBSIDIAN_ROOT + md_file, 'w') as file:
        # writes frontmatter for md file
        file.write('---\n')
        for key in md_frontmatter:
            file.write(f'{key}: {md_frontmatter[key]}\n')
        file.write('---\n\n')

        file.write(markdown)  # writes markdown template

subprocess.run(['python', 'auto_sorter.py'])
