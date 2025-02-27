from django.shortcuts import render
from rest_framework import generics
from .serializers import MovieSerializer
from .models import Movie


class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer


class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer