import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ARRAY, JSON
database_url='postgresql://postgres:vivov913@localhost:5432/Movies'
engine = create_engine(database_url)
base=declarative_base()

class Movie(base):
    __tablename__='movies'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    poster_url=Column(String)
    reviews = Column(ARRAY(String))
    processed_reviews = Column(ARRAY(String))
    sentiment_scores = Column(ARRAY(JSON))

base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()

# Query all movies
movies = session.query(Movie).all()

# Convert to a list of dictionaries
movies_list = [
    {
        'id': movie.id,
        'title': movie.title,
        'poster_url': movie.poster_url,
        'reviews': movie.reviews,
        'processed_reviews': movie.processed_reviews,
        'sentiment_scores': movie.sentiment_scores
    }
    for movie in movies
]

# Save to a JSON file
with open('movies.json', 'w') as f:
    json.dump(movies_list, f, indent=4)
