from django.urls import path
import thoughtkeeper.views


app_name = 'thoughtkeeper'
urlpatterns = [
    path('intention/books/<int:pk>/commit', thoughtkeeper.views.CommitIntentionView.as_view(), name='commit_intention'),
    path('marginnote/books/<int:pk>/leave', thoughtkeeper.views.LeaveMarginNoteView.as_view(), name='leave_marginnote'),
    path('feedback/books/<int:pk>/leave', thoughtkeeper.views.LeaveFeedbackView.as_view(), name='leave_feedback'),
]
