import frontmatter

def get_frontmatter(file):
    return frontmatter.load(file)
