from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination

from .models import Author, Song, Album, Genre, UserSongPlay
from .serializers import SongSerializer, AuthorSerializer, AlbumSerializer, GenreSerializer, SongReadSerializer, \
    UserSongPlaySerializer
from utils import convert_form_to_data
from exceptions import NO_PK_PROVIDED, OBJECT_NOT_EXIST

from users.permissions import IsOwnerOrPostOnly, IsSuperUser, IsOwner


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class ShortSongView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrPostOnly,)
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        query_param_to_model = {
            'song_id': (Song, False, {}),
            'genre_id': (Genre, True, {}),
            'author_id': (Author, True, {'authors': False}),
            'album_id': (Album, True, {'album': False}),
        }
        query_params = request.query_params

        query_count = 0
        for key in query_params:
            query_count += query_params.get(key, 0) != 0
        if query_count > 1:
            raise exceptions.ParseError({"Request": "Too many query parameters"})

        for key, value in query_params.items():
            if value is None:
                continue
            model, many, context = query_param_to_model[key]
            try:
                obj = model.objects.get(pk=value)
            except model.DoesNotExist:
                raise exceptions.NotFound(OBJECT_NOT_EXIST(model))
            obj = obj.songs if many else obj
            serializer = SongReadSerializer(obj, many=many, context=context)
            return Response(serializer.data, status=200)


class SongView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrPostOnly,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Song))
        serializer = SongSerializer(song, context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request):
        form_data = convert_form_to_data(request.data)
        serializer = SongSerializer(data=form_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Song))
        self.check_object_permissions(request, song)
        form_data = convert_form_to_data(request.data)

        serializer = SongSerializer(data=form_data, instance=song, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class AlbumView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrPostOnly,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Album))
        serializer = AlbumSerializer(album, context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request):
        form_data = convert_form_to_data(request.data)
        serializer = AlbumSerializer(data=form_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Album))
        self.check_object_permissions(request, album)
        form_data = convert_form_to_data(request.data)

        serializer = AlbumSerializer(instance=album, data=form_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class AuthorView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrPostOnly,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Author))
        serializer = AuthorSerializer(author, context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request):
        form_data = convert_form_to_data(request.data)
        serializer = AuthorSerializer(data=form_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            raise exceptions.ParseError(NO_PK_PROVIDED)

        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise exceptions.NotFound(OBJECT_NOT_EXIST(Author))
        self.check_object_permissions(request, author)
        form_data = convert_form_to_data(request.data)

        serializer = AuthorSerializer(instance=author, data=form_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class UserSongPlayView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            plays = UserSongPlay.objects.filter(user=request.user)
            serializer = UserSongPlaySerializer(plays, many=True)
            return Response(serializer.data, status=200)
        else:
            try:
                play = UserSongPlay.objects.get(song_id=pk, user=request.user)
            except Author.DoesNotExist:
                raise exceptions.NotFound(OBJECT_NOT_EXIST(Author))
            serializer = UserSongPlaySerializer(play, context={'request': request})
            return Response(serializer.data, status=200)

    def post(self, request):
        serializer = UserSongPlaySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class GenreListCreateView(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
