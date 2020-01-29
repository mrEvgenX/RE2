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

    def shelved_by_user(self, user):
        return self.shelvedbook_set.filter(user__id=user.id).first()


# TODO сделать связь книги не с юзером, а с полкой
class Shelf(models.Model):
    name = models.CharField(max_length=140)

    DEFAULT_SHELF_ID = 1


class ShelvedBookManager(models.Manager):

    def shelved_by_user(self, user):
        qs = self.get_queryset()
        qs = qs.filter(user=user)
        return qs

    def get_by_status_by_user(self, user, status, limit=None):
        qs = self.get_queryset()
        if not limit:
            return qs.filter(user=user, status=status)
        return qs.filter(user=user, status=status)[:limit]

    def counter_by_status_by_user(self, user, status):
        return self.get_by_status_by_user(user, status).count()


class ShelvedBook(models.Model):
    WANT_TO_READ = 0
    CURRENTLY_READING = 1
    READ = 2
    STATUSES = (
        (WANT_TO_READ, 'Want to read'),
        (CURRENTLY_READING, 'Currently reading'),
        (READ, 'Read'),
    )

    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shelf = models.ForeignKey(to=Shelf, on_delete=models.CASCADE, default=Shelf.DEFAULT_SHELF_ID)
    status = models.IntegerField(choices=STATUSES, default=WANT_TO_READ)  # TODO remove, give all functions to "shelf"
    started = models.DateField(null=True, blank=True)
    finished = models.DateField(null=True, blank=True)

    objects = ShelvedBookManager()

    class Meta:
        unique_together = ('book', 'user')
