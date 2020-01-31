from django.conf import settings
from django.db import models


class Note(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entity = models.ForeignKey(to=settings.THOUGHTKEEPER_ENTITY_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        abstract = True


class IntentionNote(Note):
    is_private = models.BooleanField(default=False)

    def user_can_see(self, user):
        return user == self.author or not self.is_private

    class Meta:
        unique_together = ('author', 'entity')


class MarginNote(Note):
    is_private = models.BooleanField(default=False)

    def user_can_see(self, user):
        return user == self.author or not self.is_private


class Feedback(Note):
    MAX_RATING = 5
    RATINGS = ((r, str(r)) for r in range(1, MAX_RATING + 1))
    rating = models.IntegerField(choices=RATINGS)

    class Meta:
        unique_together = ('author', 'entity')
