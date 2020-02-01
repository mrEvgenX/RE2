from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404
from booktracker.models import Book, Shelf, ShelvedBook
from booktracker.forms import ShelvingForm, MoveToShelfForm


class ListAllBooks(ListView):
    model = Book


class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            form = ShelvingForm(initial={'book': self.object.id, 'user': self.request.user.id})
            shelved_book = self.object.shelved_by_user(self.request.user)
            if not shelved_book:
                ctx.update({
                    'add_form': form,
                    'margin_notes': [],
                })
            else:
                move_to_shelf_form = MoveToShelfForm(initial={'shelf': shelved_book.shelf})
                ctx.update({
                    'remove_form': form,
                    'move_to_shelf_form': move_to_shelf_form,
                    'margin_notes': self.object.marginnotes_of_user(self.request.user),
                    'intention_note': self.object.intentionnote_of_user(self.request.user),
                    'feedback_note': self.object.feedback_of_user(self.request.user),
                })
        return ctx


class ShelveView(LoginRequiredMixin, CreateView):
    form_class = ShelvingForm
    template_name = 'booktracker/shelve.html'

    def get_initial(self):
        return {
            'book': self.get_book().id,
            'user': self.request.user.id,
        }

    def form_valid(self, form):
        self.request.user.book_set.add(self.get_book())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('booktracker:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_book(self):
        return Book.objects.get(pk=self.kwargs['pk'])


class DeshelveView(LoginRequiredMixin, DeleteView):
    model = ShelvedBook
    template_name = 'booktracker/deshelve.html'

    def get_success_url(self):
        return reverse('booktracker:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        b = get_object_or_404(Book, pk=self.kwargs['pk'])
        return get_object_or_404(b.shelvedbook_set, user__id=self.request.user.id)


class MyShelf(LoginRequiredMixin, ListView):
    template_name = 'booktracker/profile.html'

    def get_queryset(self):
        return Shelf.objects.filter(owner__username = self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'book_counters': Shelf.objects.get_summary(self.request.user),
            'shelf_owner': get_object_or_404(get_user_model(), username=self.kwargs['username'])
        })
        return ctx


class MoveToShelfView(LoginRequiredMixin, UpdateView):
    form_class = MoveToShelfForm

    def get_queryset(self):
        return ShelvedBook.objects.shelved_by_user(self.request.user)

    def get_success_url(self):
        return reverse('booktracker:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        b = get_object_or_404(Book, pk=self.kwargs['pk'])
        return get_object_or_404(b.shelvedbook_set, shelf__owner=self.request.user)
