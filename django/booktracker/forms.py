from django import forms
from django.contrib.auth import get_user_model
from booktracker.models import ShelvedBook, Book


class ShelvingForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Book.objects.all(),
        disabled=True,
    )
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True,
    )

    class Meta:
        model = ShelvedBook
        fields = ['book', 'user']


class MoveToShelfForm(forms.ModelForm):

    class Meta:
        model = ShelvedBook
        fields =['shelf']
