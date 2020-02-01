from django.urls import path
import booktracker.views
import thoughtkeeper.views


app_name = 'booktracker'
urlpatterns = [
    path('books/<int:pk>', booktracker.views.BookDetail.as_view(), name='book_detail'),
    path('books/<int:pk>/shelve', booktracker.views.ShelveView.as_view(), name='shelve'),
    path('books/<int:pk>/deshelve', booktracker.views.DeshelveView.as_view(), name='deshelve'),
    path('books/<int:pk>/move_to_shelf', booktracker.views.MoveToShelfView.as_view(), name='move_to_shelf'),

    path('books/<int:pk>/commit_intention', thoughtkeeper.views.CommitIntentionView.as_view(), name='commit_intention'),
    path('books/<int:pk>/leave_marginnote', thoughtkeeper.views.LeaveMarginNoteView.as_view(), name='leave_marginnote'),
    path('books/<int:pk>/leave_feedback', thoughtkeeper.views.LeaveFeedbackView.as_view(), name='leave_feedback'),

    #path('profile', booktracker.views.MyShelf.as_view(), name='profile'),
    #path('profile/edit', booktracker.views.MyShelf.as_view(), name='profile'),
    path('profile/<slug:username>', booktracker.views.MyShelf.as_view(), name='profile'),
    #path('profile/<slug:username>/shelf_content/<int:pk>', booktracker.views.MyShelf.as_view(), name='profile'),

    path('books/<int:entity_id>/drop_intention/<int:pk>', thoughtkeeper.views.DropIntentionView.as_view(),
         name='drop_intention'),
    path('books/<int:entity_id>/remove_marginnote/<int:pk>', thoughtkeeper.views.RemoveMarginNoteView.as_view(),
         name='remove_marginnote'),
    path('books/<int:entity_id>/remove_feedback/<int:pk>', thoughtkeeper.views.RemoveFeedbackView.as_view(),
         name='remove_feedback'),
    path('', booktracker.views.ListAllBooks.as_view(), name='all_books'),
]
