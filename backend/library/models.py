from django.db import models
from users.models import User


class Song(models.Model):
    title = models.CharField(max_length=100)
    audio = models.FileField(upload_to='tracks/')
    picture = models.ImageField(upload_to='pictures/tracks/', default='pictures/tracks/default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    users_plays = models.ManyToManyField(User, through='UserSongPlay', related_name='songs_user_played', blank=True)
    genres = models.ManyToManyField('Genre', related_name='songs')
    album = models.ForeignKey('Album', related_name='songs', on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author', related_name='songs')


class UserSongPlay(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = (('song', 'user'),)


class Album(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pictures/albums/', default='pictures/albums/default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Author', related_name='albums', on_delete=models.CASCADE)


class Author(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pictures/albums/', default='pictures/albums/default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_authors')
    created_at = models.DateTimeField(auto_now_add=True)


class Genre(models.Model):
    title = models.CharField(max_length=30, unique=True)
