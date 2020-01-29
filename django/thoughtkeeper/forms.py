from django import forms
from django.contrib.auth import get_user_model
from thoughtkeeper.models import IntentionNote


# TODO нужно грамотно оформить, как вроде get_user_model
def get_entity_model():
    from booktracker.models import Book
    return Book


class IntentionCommitForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True,
    )
    entity = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_entity_model().objects.all(),
        disabled=True,
    )

    class Meta:
        model = IntentionNote
        fields = ['author', 'entity', 'body', 'is_private']
