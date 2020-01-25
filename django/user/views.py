from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.urls import reverse


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('user:login')


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'

    def get_object(self, queryset=None):
        return self.request.user
