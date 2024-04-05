from django import template
from ..models import *
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Avg, Count

register = template.Library()


@register.inclusion_tag('partials/new_films.html')
def new_film(count=6):
    movies = Movie.published.all()[:count]
    context = {
        'movies': movies
    }
    return context


@register.inclusion_tag('partials/popular_movies.html')
def popular_movies(count=7):
    pop_movies = Movie.published.annotate(count_comment=Count('movie_comments')).order_by('-count_comment')[:count]
    context = {
        'movies': pop_movies
    }
    return context


@register.inclusion_tag('partials/popular_movies.html', name='most_selling')
def best_selling_movies(count=7):
    top_movies = Movie.published.annotate(count_selling=Count('movie_tickets')).order_by('-count_selling')[:count]
    context = {
        'movies': top_movies
    }
    return context
