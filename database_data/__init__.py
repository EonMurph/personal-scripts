from sqlalchemy import ForeignKey, Table, Column, String, Integer, Boolean, update
from sqlalchemy.orm import relationship, declarative_base
from random import choice

Base = declarative_base()

# Create movie -> genre association table
movie_genre_association_table = Table(
    'movie_genre_associations',
    Base.metadata,
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_name', ForeignKey('genres.name')),
)

# Create show -> genre association table
show_genre_association_table = Table(
    'show_genre_associations',
    Base.metadata,
    Column('show_id', ForeignKey('shows.id')),
    Column('genre_name', ForeignKey('genres.name'))
)


# Initialise the Movie model for movie entries
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    watched = Column(Boolean, default=False)
    genres = relationship(
        'Genre', secondary=movie_genre_association_table, back_populates='movies', cascade='merge')  # creates relationship between genre and movie

    def __repr__(self):
        return f"Movie: {self.name} ({self.year}) {self.genres}. Watched: {self.watched}"


# Initialise the Show model for show entries
class Show(Base):
    __tablename__ = 'shows'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    watched = Column(Boolean, default=False)
    genres = relationship(
        'Genre', secondary=show_genre_association_table, back_populates='shows', cascade='merge')  # creates relationship between show and genre

    def __repr__(self):
        return f"Show: {self.name} ({self.year}) {self.genres}. Watched: {self.watched}"


# Initialise Genre model for genre entries
class Genre(Base):
    __tablename__ = 'genres'

    name = Column(String, primary_key=True)
    # Create movie -> genre and show -> genre relationships
    movies = relationship(
        'Movie', secondary=movie_genre_association_table, back_populates='genres', cascade='merge')
    shows = relationship(
        'Show', secondary=show_genre_association_table, back_populates='genres', cascade='merge')

    def __repr__(self):
        return f"Genre: {self.name}"


# Create list of genres for initialisation within the database
list_of_genres = {
    'comedy': Genre(name='comedy'),
    'action': Genre(name='action'),
    'romance': Genre(name='romance'),
    'family': Genre(name='family'),
}


def str_to_class(classname):
    class_names = {'Movie': Movie, 'Show': Show, 'Genre': Genre}
    return class_names[classname]


# Create function for adding movies to the database
def add_movie(data, session):
    movie = Movie(name=data['name'], year=data['year'])
    session.add(movie)

    movie_query = session.query(Movie).filter(
        Movie.name == data['name'], Movie.year == data['year'])  # specifies movie entry to add genres to
    for genre in data['genres']:
        movie.genres.append(
            session.query(Genre).filter(Genre.name == genre).first())


# Create function for adding shows to the database
def add_show(data, session):
    show = Show(name=data['name'], year=data['year'])
    session.add(show)

    show_query = session.query(Show).filter(
        Show.name == data['name'], Show.year == data['year'])  # specifies show entry to add genres to
    for genre in data['genres']:
        show.genres.append(
            session.query(Genre).filter(Genre.name == genre).first())


def update_show(data, session):
    name = data['name']
    year = data['year']
    if data['watched'] is not None:
        # Create dict with watched boolean for update function
        update_values = {'watched': data['watched']}
    else:
        update_values = data['update_values']

    session.query(Show).filter(Show.name == name,
                               Show.year == year).update(update_values)


def update_movie(data, session):
    name = data['name']
    year = data['year']
    if 'watched' in data.keys():
        update_values = {'watched': data['watched']}
    else:
        update_values = data['update_values']

    session.query(Movie).filter(Movie.name == name,
                                Movie.year == year).update(update_values)


# def get_movie(session, genre=None):
#     movies = [movie for movie in session.query(
#         Movie).filter(Movie.watched == False).all()]  # gets list of movies in db
#     if genre is not None:
#         matching_movies = [
#             movie for movie in movies if genre in str(movie.genres)]
#         if len(matching_movies) != 0:
#             print(choice(matching_movies))
#         else:
#             print('No movie matches requirements.')
#     else:
#         print(choice(movies))


# def get_show(session, genre=None):
#     shows = [show for show in session.query(
#         Show).filter(Show.watched == False).all()]
#     if genre is not None:
#         matching_shows = [
#             show for show in shows if genre in str(show.genres)]
#         if len(matching_shows) != 0:
#             print(choice(matching_shows))
#         else:
#             print('No show matches requirements.')
#     else:
#         print(choice(shows))


def get_media(session, class_type, genre=None):
    list_of_media = [media for media in session.query(
        str_to_class(class_type)).all()]
    list_of_valid_media = [
        media for media in list_of_media if media.watched == False]
    if genre is not None:
        media_with_genre = [
            media for media in list_of_valid_media if genre in str(media.genres)]
        if len(media_with_genre) != 0:
            print(choice(media_with_genre))
        else:
            print('No media matched requirements.')
    else:
        print(choice(list_of_valid_media))
