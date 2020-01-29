from django.urls import reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from thoughtkeeper.forms import IntentionCommitForm
from thoughtkeeper.forms import get_entity_model


class CommitIntentionView(LoginRequiredMixin, CreateView):
    form_class = IntentionCommitForm
    template_name = 'thoughtkeeper/commit_intention.html'

    def get_initial(self):
        return {
            'entity': self.get_entity().id,
            'author': self.request.user.id,
        }

    def get_success_url(self):
        return reverse(settings.THOUGHTKEEPER_COMMIT_INTENTION_REDIRECT, kwargs={'pk': self.kwargs['pk']})

    def get_entity(self):
        return get_entity_model().objects.get(pk=self.kwargs['pk'])
