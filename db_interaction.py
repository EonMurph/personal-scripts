from sqlalchemy.orm import sessionmaker
from database_data import *
from sqlalchemy import create_engine, MetaData
from ast import literal_eval
import argparse
from argparse import RawTextHelpFormatter
import yaml

print('pay deposit')
print('pay deposit')
print('pay deposit')
print('pay deposit')
print('pay deposit')
print('pay deposit')

# Initialise terminal arguments
parser = argparse.ArgumentParser(
    description="deletes, updates, and adds to a database based on inputted dicts", formatter_class=RawTextHelpFormatter)
# creates group so that arguments are mutually exclusive
action_type_group = parser.add_mutually_exclusive_group(required=True)

action_type_group.add_argument('--add', type=str, nargs='*',
                               help='''use if populating the database; 
                               follow with:
                                    input_type,
                                    media type,
                                    and either dict or file''')
action_type_group.add_argument('-upd', '--update', type=str, nargs='*',
                               help='''use if updating a row in the database; 
                               follow with class name of type and dict of key values pairs:
                                    update_values: dictionary;
                                        key: column, value: value
                                    condition: items;
                                        key: 'name' value: <name of media>,
                                        key: 'year' value: <year of release>''')
action_type_group.add_argument('-del', '--delete', type=str, nargs='*',
                               help='''use if deleting a row in the database; 
                               follow with class name of type and row name and year''')
action_type_group.add_argument('--watched', type=str, nargs='*',
                               help='''use if setting a movie or show to watched;
                               follow with: 
                                    input_type,
                                    media type,
                                    and either a dict or file
                                    (if dict, then follow format as follows:
                                        key: 'watched', value: boolean,
                                        key: 'name',  value: <name of media>,
                                        key: 'year' value: <year of release>)''')
action_type_group.add_argument('--query', type=str, nargs='*',
                               help='''use if asking for a movie;
                               follow with media type and genre, if you want specific genre''')


args = parser.parse_args()

# Initialise SQLAlchemy values
engine = create_engine('sqlite:///katelyn.sqlite3')
Base.metadata.create_all(engine)
meta = MetaData()
MetaData.reflect(meta, bind=engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


# Add any unregistered genres to database
for genre in list_of_genres:
    if (query := session.query(Genre).filter(Genre.name == genre)).first() == None:
        session.add(list_of_genres[genre])
    else:
        continue

if args.add is not None:
    if args.add[0] == 'dict':
        entry = literal_eval(args.add[2])  # turns entry string into dictionary
        if args.add[1] == 'Movie':
            add_movie(entry, session)
        elif args.add[1] == 'Show':
            add_show(entry, session)

    elif args.add[0] == 'file':
        with open(args.add[1], 'r') as yaml_file:
            list_of_media = yaml.safe_load(yaml_file)

            if (movies := list_of_media['Movie']) is not None:
                for movie in movies:
                    entry = movies.get(movie)
                    add_movie(entry, session)

            if (shows := list_of_media['Show']) is not None:
                for show in shows:
                    entry = shows.get(show)
                    add_show(entry, session)

elif args.update is not None:
    entry = literal_eval(args.update[1])

    if args.update[0] == 'Show':
        update_show(entry, session)
    if args.update[0] == 'Movie':
        update_movie(entry, session)

elif args.watched is not None:
    if args.watched[0] == 'dict':
        entry = literal_eval(args.watched[2])

        if args.watched[1] == 'Show':
            update_show(entry, session)

        if args.watched[1] == 'Movie':
            update_movie(entry, session)

    if args.watched[0] == 'file':
        with open(args.watched[1], 'r') as yaml_file:
            list_of_media = yaml.safe_load(yaml_file)

            if (movies := list_of_media['Movie']) is not None:
                for movie in movies:
                    entry = movies.get(movie)
                    update_movie(entry, session)
            if (shows := list_of_media['Show']) is not None:
                for show in shows:
                    entry = shows.get(show)
                    update_show(entry, session)

elif args.delete is not None:
    entry = literal_eval(args.delete[1])
    name = entry['name']
    year = entry['year']

    if args.delete[0] == 'Show':
        session.query(Show).filter(
            Show.name == name, Show.year == year).delete()
    if args.delete[0] == 'Movie':
        session.query(Movie).filter(
            Movie.name == name, Movie.year == year).delete()

elif args.query is not None:
        try:
            genre = args.query[1]
            get_media(session, args.query[0], genre)
        except IndexError:
            get_media(session, args.query[0])

session.commit()
