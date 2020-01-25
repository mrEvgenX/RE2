from django.urls import path
from booktracker.views import ListAllBooks, BookDetail, ShelveView, MyShelf, DeshelveView


app_name = 'booktracker'
urlpatterns = [
    path('', ListAllBooks.as_view(), name='all_books'),
    path('books/<int:pk>', BookDetail.as_view(), name='book_detail'),
    path('books/<int:pk>/shelve', ShelveView.as_view(), name='shelve'),
    path('books/<int:pk>/deshelve', DeshelveView.as_view(), name='deshelve'),
    path('shelf/', MyShelf.as_view(), name='shelf'),
]
