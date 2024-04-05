import json

from app.models import Movie

# from .models import Movie

with open('fixtures/movies.json', 'r') as fj:
    py_dict = json.load(fj)
    for key in py_dict.items():
        Movie.objects.create(title=key[1]['title'], release_year=key[1]['release_year'], play_time
            =key[1]['play_time'])


