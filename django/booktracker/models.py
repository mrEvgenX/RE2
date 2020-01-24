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


class Book(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='books')
    year = models.IntegerField()
    publisher = models.CharField(max_length=140, null=True, blank=True)
    description = models.TextField()
    shelved_by = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through='ShelvedBook',
    )

    def __str__(self):
        return '{} "{}"'.format(self.author, self.title)


class ShelvedBook(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started = models.DateField()
    finished = models.DateField()

    class Meta:
        unique_together = ('book', 'user')
