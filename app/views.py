from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail

from app.models import Movie, Seat


def cinema_list(request):
    cinema = Cinema.objects.all()
    context = {
        'cinema': cinema
    }
    return render(request, 'app/movie_theaters.html', context)


def list_movies(request, category=None, pk=None):
    cinema = None
    if category is None:
        if pk is None:
            movies = Movie.published.all()
        else:
            cinema = Cinema.objects.get(pk=pk)
            movies = Movie.published.filter(cinema=cinema)
    else:
        movies = Movie.published.filter(category=category)

    context = {
        'movies': movies,
        'category': category,
        'cinema': cinema
    }

    return render(request, 'app/movies.html', context)


def list_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = movie.movie_comments.all()
    form = CommentForm()
    seats = Seat.objects.filter(is_given=False, movie=movie)

    context = {
        'comments': comments,
        'form': form,
        'movie': movie,
        'seats': seats
    }
    return render(request, 'app/seats.html', context)


@login_required()
def reserve_seat(request, movie_id, seat_id):
    movie = Movie.objects.get(id=movie_id)
    # return render(request, '', movie)
    seat = Seat.objects.get(id=seat_id)
    Ticket.objects.create(movie=movie, user=request.user, seat=seat)
    seat.is_given = True
    seat.save()
    messages.success(request, 'بلیط شما با موفقیت صادر گردید')
    return redirect('app:list_seats', movie_id)


def stats(request):
    pass


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.clean_password())
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def movie_comment(request, pk):
    if 'comment' in request.POST:
        movie = get_object_or_404(Movie, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.save()
            messages.success(request, 'کامنت شما با موفقیت ارسال شد')
            return redirect('app:list_seats', movie.id)
    else:
        form = CommentForm()
    return render(request, 'app/seats.html', {'form': form})


@login_required()
def profile(request):
    user = request.user
    tickets = user.tickets.all()
    context = {
        'tickets': tickets,
        'user': user
    }
    return render(request, 'app/profile.html', context)


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'app/ticket_detail.html', {'ticket': ticket})


def response_to_check(request):
    user = request.user
    check = Check.objects.filter(user=user)
    context = {
        'tickets': check
    }
    return render(request, 'app/response-check.html', context)


def create_check(request):
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            messsage = None
            subject = 'تیکت ارسالی از کاربر'
            send_mail(subject, form['body'], 'barzansalimpour5@gmail.com', ['salimpouranand@gmail.com']
                      , fail_silently=False)
            Check.objects.create(user=request.user, name=form['name'], body=form['body'])
            return redirect('app:list_movies')
    else:
        form = CheckForm()
    context = {
        'form': form
    }
    return render(request, 'forms/check.html', context)


def index(request):
    context = {

    }
    return render(request, 'app/index.html', context)


def search(request):
    movies = None
    if 'query' in request.GET:
        query = request.GET['query']
        # search_query = SearchQuery(query)
        # search_vector = SearchVector('title', weight='A') + SearchVector('category', weight='A') \
        #                 + SearchVector('description', weight='B')
        movies1 = Movie.published.annotate(similarity=TrigramSimilarity('title', query)) \
            .filter(similarity__gt=.1).order_by('-similarity')
        movies2 = Movie.published.annotate(similarity=TrigramSimilarity('description', query)) \
            .filter(similarity__gt=.1).order_by('-similarity')
        movies3 = movies2 | movies1
    context = {
        'movies': movies3
    }
    return render(request, 'app/search.html', context)


