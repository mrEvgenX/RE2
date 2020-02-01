from django import forms
from booktracker.models import ShelvedBook, Book, Shelf


class ShelvingForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Book.objects.all(),
        disabled=True,
    )
    shelf = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Shelf.objects.all(),
        disabled=True,
    )

    class Meta:
        model = ShelvedBook
        fields = ['book', 'shelf']


class MoveToShelfForm(forms.ModelForm):

    class Meta:
        model = ShelvedBook
        fields =['shelf']
