from django.db import models
from django.conf import settings


class Author(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    patronymic = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        if self.patronymic:
            return '{} {} {}'.format(self.first_name, self.patronymic, self.last_name)
        return '{} {}'.format(self.first_name, self.last_name)


class ShelfManager(models.Manager):

    def get_summary(self, user):
        qs = self.get_queryset()
        qs = qs.filter(owner=user).annotate(num_books=models.Count('book'))
        return qs


class Shelf(models.Model):
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_defined = models.BooleanField(null=False, default=False)
    default = models.BooleanField(null=False, default=False)

    objects = ShelfManager()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='books')
    year = models.IntegerField()
    publisher = models.CharField(max_length=140, null=True, blank=True)
    description = models.TextField()
    shelved_to = models.ManyToManyField(to=Shelf, through='ShelvedBook')

    def __str__(self):
        return '{} "{}"'.format(self.author, self.title)

    def shelved_by_user(self, user):
        return self.shelvedbook_set.filter(shelf__owner=user).first()

    def marginnotes_of_user(self, user):
        return self.marginnote_set.filter(author=user).all()

    def intentionnote_of_user(self, user):
        return self.intentionnote_set.filter(author=user).first()

    def feedback_of_user(self, user):
        return self.feedback_set.filter(author=user).first()


class ShelvedBookManager(models.Manager):

    def shelved_by_user(self, user):
        qs = self.get_queryset()
        qs = qs.filter(shelf__owner=user)
        return qs


class ShelvedBook(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    shelf = models.ForeignKey(to=Shelf, on_delete=models.CASCADE)
    started = models.DateField(null=True, blank=True)
    finished = models.DateField(null=True, blank=True)

    objects = ShelvedBookManager()

    class Meta:
        unique_together = ('book', 'shelf')
