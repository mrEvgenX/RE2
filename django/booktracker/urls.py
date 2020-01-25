from django.urls import path
from booktracker.views import ListAllBooks, BookDetail


app_name = 'booktracker'
urlpatterns = [
    path('', ListAllBooks.as_view(), name='all_books'),
    path('books/<int:pk>', BookDetail.as_view(), name='book_detail'),
]
