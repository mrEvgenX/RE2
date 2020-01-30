from django.urls import path
import booktracker.views
import thoughtkeeper.views


app_name = 'booktracker'
urlpatterns = [
    path('', booktracker.views.ListAllBooks.as_view(), name='all_books'),
    path('books/<int:pk>', booktracker.views.BookDetail.as_view(), name='book_detail'),
    path('books/<int:pk>/shelve', booktracker.views.ShelveView.as_view(), name='shelve'),
    path('books/<int:pk>/deshelve', booktracker.views.DeshelveView.as_view(), name='deshelve'),
    path('shelf/', booktracker.views.MyShelf.as_view(), name='shelf'),
    path('books/<int:pk>/change_status', booktracker.views.ChangeStatusView.as_view(), name='change_status'),
    path('books/<int:pk>/commit_intention', thoughtkeeper.views.CommitIntentionView.as_view(), name='commit_intention'),
    path('books/<int:pk>/leave_marginnote', thoughtkeeper.views.LeaveMarginNoteView.as_view(), name='leave_marginnote'),
    path('books/<int:pk>/leave_feedback', thoughtkeeper.views.LeaveFeedbackView.as_view(), name='leave_feedback'),
]
