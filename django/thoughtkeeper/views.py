from django.urls import reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
import thoughtkeeper.forms


class PostNoteView(CreateView):
    template_name = 'thoughtkeeper/post_note.html'
    page_title = None
    page_description = None

    def get_initial(self):
        return {
            'entity': self.get_entity().id,
            'author': self.request.user.id,
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': self.page_title,
            'description': self.page_description,
        })
        return ctx

    def get_success_url(self):
        return reverse(settings.THOUGHTKEEPER_COMMIT_INTENTION_REDIRECT, kwargs={'pk': self.kwargs['pk']})

    def get_entity(self):
        return thoughtkeeper.forms.get_entity_model().objects.get(pk=self.kwargs['pk'])


class CommitIntentionView(LoginRequiredMixin, PostNoteView):
    form_class = thoughtkeeper.forms.IntentionCommitForm
    page_title = 'Commit intention'
    page_description = 'Write your expectations about the book.'


class LeaveMarginNoteView(LoginRequiredMixin, PostNoteView):
    form_class = thoughtkeeper.forms.LeaveMarginNoteForm
    page_title = 'Jot down something'
    page_description = 'Place here your insights, quotes you liked or anything you found to be usefull.'


class LeaveFeedbackView(LoginRequiredMixin, PostNoteView):
    form_class = thoughtkeeper.forms.LeaveFeedbackForm
    page_title = 'Leave feedback'
    page_description = 'What do you think about it?'
