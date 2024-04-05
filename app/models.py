from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# from django.contrib.gis.db import models as gis_models
from django_jalali.db import models as jmodels


# Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publish=True)


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CustomUser2(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    location_name = models.CharField(max_length=100, null=True)
    # location = gis_models.PointField(null=True, blank=True)


class Movie(models.Model):
    CATEGORY_CHOICES = (
        ('طنز', 'طنز'),
        ('عاشقانه', 'عاشقانه'),
        ('خشن', 'خشن'),
        ('انیمیشن', 'انیمیشن'),
        ('سایر', 'سایر')
    )
    cinema = models.ManyToManyField(Cinema, related_name='movies')
    title = models.CharField(max_length=100)
    release_year = models.IntegerField()
    play_time = jmodels.jDateTimeField(default=00-00-00)
    description = models.TextField(null=True)
    publish = models.BooleanField(default=False)
    image = models.ImageField(upload_to='film%Y%m%d', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='سایر')
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('app:list_seats', args=[self.pk])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    # objects
    objects = models.Manager()
    published = PublishedManager()


class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_seats', null=True)
    number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=1)
    off = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_given = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"number: {self.number}"

    # manager
    objects = models.Manager()


class Ticket(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_tickets')
    user = models.ForeignKey(CustomUser2, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='tickets')
    date_bought = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'seat')
        ordering = ['-date_bought']
        indexes = [
            models.Index(fields=['-date_bought'])
        ]


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Comment_For_Player(models.Model):
    user = models.ForeignKey(CustomUser2, on_delete=models.CASCADE, related_name='user_comments')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Check(models.Model):
    user = models.ForeignKey(CustomUser2, on_delete=models.CASCADE, related_name='checks')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Response(models.Model):
    ticket = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='check_responses')
    responser = models.CharField(max_length=100)
    body = models.TextField()
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class CommentResponse(models.Model):
    movie = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_responses')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
