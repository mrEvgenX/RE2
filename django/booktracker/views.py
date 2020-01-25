from django.views.generic import ListView, DetailView
from booktracker.models import Book


class ListAllBooks(ListView):
    model = Book


class BookDetail(DetailView):
    model = Book
