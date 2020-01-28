from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from booktracker.models import Book, ShelvedBook
from booktracker.forms import ShelvingForm, ChangeStatusForm


class ListAllBooks(ListView):
    model = Book


class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            form  = ShelvingForm(initial={'book': self.object.id, 'user': self.request.user.id})
            shelved_book = self.object.shelved_by_user(self.request.user)
            if not shelved_book:
                ctx.update({'add_form': form})
            else:
                change_status_form = ChangeStatusForm(initial={'status': shelved_book.status})
                ctx.update({'remove_form': form, 'reading_status': shelved_book.get_status_display(), 'change_status_form': change_status_form})
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
        return ShelvedBook.objects.shelved_by_user(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'books_want_to_read': ShelvedBook.objects.get_by_status_by_user(self.request.user, ShelvedBook.WANT_TO_READ),
            'books_currently_reading': ShelvedBook.objects.get_by_status_by_user(self.request.user, ShelvedBook.CURRENTLY_READING),
            'books_read': ShelvedBook.objects.get_by_status_by_user(self.request.user, ShelvedBook.READ, 10),
            'want_to_read_counter': ShelvedBook.objects.counter_by_status_by_user(self.request.user, ShelvedBook.WANT_TO_READ),
            'currently_reading_counter': ShelvedBook.objects.counter_by_status_by_user(self.request.user, ShelvedBook.CURRENTLY_READING),
            'read_counter': ShelvedBook.objects.counter_by_status_by_user(self.request.user, ShelvedBook.READ)
        })
        return ctx


class ChangeStatusView(LoginRequiredMixin, UpdateView):
    form_class = ChangeStatusForm

    def get_queryset(self):
        return ShelvedBook.objects.shelved_by_user(self.request.user)

    def get_success_url(self):
        return reverse('booktracker:book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        b = get_object_or_404(Book, pk=self.kwargs['pk'])
        return get_object_or_404(b.shelvedbook_set, user__id=self.request.user.id)

    # def form_invalid(self, form):
    #     return HttpResponseRedirect(redirect_to=self.object.question.get_absolute_url())