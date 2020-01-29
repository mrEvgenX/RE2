from django.urls import path
import thoughtkeeper.views


app_name = 'thoughtkeeper'
urlpatterns = [
    path('intention/books/<int:pk>/commit', thoughtkeeper.views.CommitIntentionView.as_view(), name='commit_intention'),
]
