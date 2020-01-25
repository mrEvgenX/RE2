from django.views.generic import ListView
from booktracker.models import Book


class ListAllBooks(ListView):
    model = Book
