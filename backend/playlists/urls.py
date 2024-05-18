from django.urls import path
from .views import PlaylistView, CollectionView, PlaylistListChangeView

urlpatterns = [
    path("", PlaylistView.as_view(), name="playlists"),
    path("<int:pk>/", PlaylistView.as_view(), name="playlist"),
    path("song/", PlaylistListChangeView.as_view(), name="playlist-change"),

    path("like/<int:pk>", CollectionView.as_view(), name="song_like"),
    path("liked/", CollectionView.as_view(), name="collection"),
]