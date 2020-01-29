from django.urls import path
import booktracker.views


app_name = 'booktracker'
urlpatterns = [
    path('', booktracker.views.ListAllBooks.as_view(), name='all_books'),
    path('books/<int:pk>', booktracker.views.BookDetail.as_view(), name='book_detail'),
    path('books/<int:pk>/shelve', booktracker.views.ShelveView.as_view(), name='shelve'),
    path('books/<int:pk>/deshelve', booktracker.views.DeshelveView.as_view(), name='deshelve'),
    path('shelf/', booktracker.views.MyShelf.as_view(), name='shelf'),
    path('books/<int:pk>/change_status', booktracker.views.ChangeStatusView.as_view(), name='change_status'),
]
