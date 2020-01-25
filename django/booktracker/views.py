from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from booktracker.models import Book
from booktracker.forms import Add2ShelfForm


class ListAllBooks(ListView):
    model = Book


class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and not self.book_already_shelved():
            ctx.update({
                'form': Add2ShelfForm(initial={'book': self.object.id, 'user': self.request.user.id}),
            })
        return ctx

    def book_already_shelved(self):
        return self.request.user.book_set.filter(pk=self.object.id).exists()


class Add2Shelf(LoginRequiredMixin, CreateView):
    form_class = Add2ShelfForm
    template_name = 'booktracker/add2shelf.html'

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


class MyShelf(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'booktracker/shelf.html'

    def get_queryset(self):
        return self.request.user.book_set.all()
