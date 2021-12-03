from django.db import models
from likes.models import Like
from django.contrib.contenttypes.fields import GenericRelation


class CreatedAt(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(CreatedAt):
    description = models.TextField()
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='post')
    likes = GenericRelation(Like)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author}'


class Picture(CreatedAt):
    image = models.ImageField(upload_to='pictures', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pictures')

