import yaml, argparse
from datetime import date
from pathlib import Path

# creates arguments for command line
parser = argparse.ArgumentParser(description='creates a markdown file based on yaml file')
parser.add_argument('file', type=str, help='enter the yaml file')
parser.add_argument('type', type=str, help='enter the type of the template')
args = parser.parse_args()

md_file = 'Untitled'

with open(args.file, 'r') as yaml_file:
    template_data = list(yaml.full_load_all(yaml_file))

    for doc in template_data:
        if doc['template_type'] == (args.type):
            template = doc
            if 'title' in template:
                exec(template['title'])

    md_frontmatter = template.get('frontmatter', None)
    if 'date-created' in md_frontmatter:
        exec(md_frontmatter['date-created'])


def date_suffix(): # decides on date suffix for h1 based on last digit in day date
    if (digit := date.today().strftime('%d')[-1]) in ['1', '2', '3']:
        if digit == '1': return 'st'
        elif digit == '2': return 'nd'
        else: return 'rd'
    else: return 'th'


markdown = template['markdown'].replace('DATE-PLACEHOLDER', date.today().strftime(f'%B %d{date_suffix()}, %Y')) # replaces 'date-created' code with result

if not Path.exists(Path(md_file + '.md').absolute()):
    with open(md_file + '.md', 'w') as file:
        # writes frontmatter for md file
        file.write('---\n')
        for key in md_frontmatter:
            file.write(f'{key}: {md_frontmatter[key]}\n')
        file.write('---\n\n')

        file.write(markdown) # writes markdown template
