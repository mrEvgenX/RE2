from django.urls import path
from booktracker.views import ListAllBooks, BookDetail, Add2Shelf, MyShelf


app_name = 'booktracker'
urlpatterns = [
    path('', ListAllBooks.as_view(), name='all_books'),
    path('books/<int:pk>', BookDetail.as_view(), name='book_detail'),
    path('books/<int:pk>/add2shelf', Add2Shelf.as_view(), name='add2shelf'),
    path('shelf/', MyShelf.as_view(), name='shelf'),
]
