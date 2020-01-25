from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from booktracker.models import Book, ShelvedBook
from booktracker.forms import ShelvingForm


class ListAllBooks(ListView):
    model = Book


class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            form  = ShelvingForm(initial={'book': self.object.id, 'user': self.request.user.id})
            if not self.object.shelved_by_user(self.request.user):
                ctx.update({'add_form': form})
            else:
                ctx.update({'remove_form': form})
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
    model = Book
    template_name = 'booktracker/shelf.html'

    def get_queryset(self):
        return self.request.user.book_set.all()
