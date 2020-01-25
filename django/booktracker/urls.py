from django.contrib import admin
from django.urls import path
from booktracker.views import ListAllBooks


app_name = 'booktracker'
urlpatterns = [
    path('', ListAllBooks.as_view(), name='books_list'),
]
