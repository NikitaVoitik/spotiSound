from django.urls import path

from .views import (SongView, AuthorView, AlbumView, GenreListCreateView, GenreRetrieveUpdateDestroyView, ShortSongView,
                    UserSongPlayView)

urlpatterns = [
    path('song/short', ShortSongView.as_view(), name='short-song'),
    path('song/', SongView.as_view(), name='song'),
    path('song/<int:pk>/', SongView.as_view(), name='song_update'),
    path('play/', UserSongPlayView.as_view(), name='play'),
    path('play/<int:pk>', UserSongPlayView.as_view(), name='play'),

    path('author/', AuthorView.as_view(), name='author'),
    path('author/<int:pk>/', AuthorView.as_view(), name='author_change'),

    path('album/', AlbumView.as_view(), name='album'),
    path('album/<int:pk>/', AlbumView.as_view(), name='album_update'),

    path('genre/', GenreListCreateView.as_view(), name='genre'),
    path('genre/<int:pk>/', GenreRetrieveUpdateDestroyView.as_view(), name='genre_update'),
]
