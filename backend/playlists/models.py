from django.db import models
from library.models import Song
from users.models import User


class SongPlaylist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='picture/playlists/', default='picture/playlists/default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField(Song, through=SongPlaylist, blank=True)


class SongCollection(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# playlist of liked
class Collection(models.Model):
    picture = models.ImageField(upload_to='picture/playlists/', default='picture/playlists/collection-default.jpg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection')
    songs = models.ManyToManyField(Song, through=SongCollection, related_name='collections')
