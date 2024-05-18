from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.db.models import Q

from library.models import Song
from utils import convert_form_to_data
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from users.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .models import Playlist, Collection, SongCollection, SongPlaylist
from .serializers import CollectionSerializer, PlaylistSerializer
from exceptions import NO_PK_PROVIDED, OBJECT_NOT_EXIST


class PlaylistView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Playlist))
        self.check_object_permissions(request, playlist)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=200)

    def post(self, request):
        form_data = convert_form_to_data(request.data)
        playlist_serializer = PlaylistSerializer(data=form_data, context={'request': request})
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()

        return Response(playlist_serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Playlist))
        self.check_object_permissions(request, playlist)
        form_data = convert_form_to_data(request.data)

        serializer = PlaylistSerializer(instance=playlist, data=form_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Playlist))
        self.check_object_permissions(request, playlist)

        playlist.delete()

        return Response(status=204)


class PlaylistListChangeView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def post(self, request):
        data = request.data
        try:
            playlist = Playlist.objects.get(pk=data.get('playlist'))
            song = Song.objects.get(pk=data.get('song'))

        except Song.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Song))
        except Playlist.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Playlist))
        self.check_object_permissions(request, playlist)
        self.check_object_permissions(request, song)

        try:
            song_playlist = SongPlaylist.objects.get(Q(song=song) & Q(playlist=playlist))
            song_playlist.delete()
        except SongPlaylist.DoesNotExist:
            SongPlaylist.objects.create(song=song, playlist=playlist)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=200)


class CollectionView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            collection = Collection.objects.get(user=user)
        except Collection.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Collection))
        self.check_object_permissions(request, collection)

        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            song = Song.objects.get(pk=pk)
            collection = Collection.objects.get(user=request.user)
        except Song.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Song))
        except Collection.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Collection))

        try:
            song_collection = SongCollection.objects.get(Q(song=song) & Q(collection=collection))
            song_collection.delete()
        except SongCollection.DoesNotExist:
            SongCollection.objects.create(collection=collection, song=song)

        serializer = CollectionSerializer(collection)

        return Response(serializer.data, status=200)
