from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import *


def make_unpublish(modeladmin, request, queryset):
    result = queryset.update(publish=False)
    modeladmin.message_user(request, f"{result} فیلم در حالت غیرمنتشر قرار گرفت")


make_unpublish.short_description = 'غیر منتشر کردن موارد انتخاب شده'


def make_publish(modeladmin, request, queryset):
    result = queryset.update(publish=True)
    modeladmin.message_user(request, f"{result} فیلم منتشر گردید")


make_publish.short_description = ' منتشر کردن موارد انتخاب شده'


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0


class CommentResponseInline(admin.TabularInline):
    model = CommentResponse
    extra = 0


class CommentMovieInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ResponseInline]


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'created_at']
    inlines = [CommentResponseInline]
    list_display_links = ['name']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['movie', 'seat', 'user']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['number', 'price', 'movie']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'play_time']
    list_editable = ['play_time']
    inlines = [CommentMovieInline]
    actions = [make_unpublish, make_publish]


@admin.register(CustomUser2)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'age']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('age', 'image', 'phone')}),
    )
