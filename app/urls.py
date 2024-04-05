from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('movies', list_movies, name='list_movies'),
    path('movies/<str:category>/', list_movies, name='list_movies_by_category'),
    path('movies/None/<int:pk>/', list_movies, name='list_movies_by_cinema'),
    path('<int:movie_id>/seats', list_seats, name='list_seats'),
    path('seat/reserve/<int:movie_id>/<int:seat_id>', reserve_seat, name='reserve_seat'),
    path('profile/', profile, name='profile'),
    path('ticket_detail/<int:pk>/', ticket_detail, name='ticket_detail'),
    path('movie_comment/<int:pk>', movie_comment, name='movie_comment'),
    path('response_ticket/', response_to_check, name='response_ticket'),
    path('check', create_check, name='check'),
    path('search', search, name='search'),
    path('cinema_list', cinema_list, name='cinema_list'),
]
