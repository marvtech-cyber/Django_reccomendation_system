"""
Using Factory Boy to generate test data for testing the movie models.
unsaved_movie = MovieFactory.build() , generates model instance without saving to database.
saved_movie =  MovieFactory.create(), generatesa model instance and saves to database.
movies = MovieFactory.create_batch(5), generates and saves a specified number of instances to the database eg 5.
"""

from factory import DjangoModelFactory, Faker
from ..models import Movie

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = Faker('sentence', nb_words=4)
    genres = Faker('pylist', nb_elements=3, variable_nb_elements=True, value_types=['str'])
