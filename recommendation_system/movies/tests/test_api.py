import pytest
from django.urls import reverse
from rest_framework import status
from ..models import Movie
from .factory import (MovieFactory,)
import json
from django.test import override_settings

@pytest.mark.django_db
def test_create_movie(client):
    url = reverse("movie-api")
    data = {"title": "Star-Trek", "genres": json.dumps(["Sci-fi", "Adventure"])}

    response = client.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert Movie.objects.filter(title="Star-Trek").count() == 1

@pytest.mark.django_db
def test_retrieve_movie(client):
    movie = MovieFactory()
    url = reverse("movies:movie-api-detail", kwargs={"pk": movie.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": movie.id,
        "title": movie.title,
        "genres": movie.genres
    }

@pytest.mark.django_db
def test_update_movie(client):
    movie = MovieFactory()
    new_title = "Rambo"
    url = reverse("movies:movie-api-detail", kwargs={"pk": movie.id})
    data = {"title": new_title}

    response = client.put(url, json=data)
    assert response.status_code == status.HTTP_200_OK, response.json()
    movie = Movie.objects.filter(id=movie.id).first()
    assert movie
    assert movie.title == new_title


@pytest.mark.django_db
def test_delete_movie(client):
    movie = MovieFactory()
    url = reverse("movies:movie-api-detail", kwargs={"pk":movie.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Movie.objects.filter(id=movie.id).exists()

@pytest.mark.django_db
#overides the PAGE_SIZE setting
@override_settings(REST_FRAMEWORK={'PAGE_SIZE': 10})

def test_list_movies_with_pagination(client):
    # create a batch of movies , and adjust the number according to your PAGE_SIZE setting
    movies = MovieFactory.create_batch(10)

    # define the URL for the list movies endpoint
    url = reverse("movies:api-movie-list")

    # perform a GET request to the list endpoint
    response = client.get(url)

    # assert that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # convert the response data to JSON
    data = response.json()

    # assert the structure of the paginated response
    assert "count" in data
    assert "next" in data
    assert "previous" in data
    assert "results" in data

    # assert that the count matches the total number of movies created
    assert data["count"] == 10

    
    # assert the pagination metadata (if applicable depending on the number of items and page size)
    # for example if you expect more items and multiple pages : Assert data["next] is not None
    assert data["next"] is None
    assert data["previous"] is None

    # assert that the number of movies in the result matches the number of movies created
    # this checks the first page of results just in case of multiple pages
    assert len(data["results"]) == 10 #adjust according to page size setting


    # use a set to ensure that the returned movies match the expected movies
    returned_movie_ids = {movie["id"] for movie in data["results"]}
    expected_movie_ids = {movie.id for movie in movies}
    assert returned_movie_ids == expected_movie_ids 

    # verify that each movie in the response contains the expected keys
    for movie_data in data["results"]:
        assert set(movie_data.keys()) == {"id", "title", "genres"}