import frontmatter

def get_frontmatter(file):
    return frontmatter.load(file)

def get_date(data):
    date = data["date-created"].split("-")
    year, month = date[0], date[1]
    return year, month
