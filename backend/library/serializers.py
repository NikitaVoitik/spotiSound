from rest_framework import serializers
from utils import validate_exist_and_return_array, validate_exist_and_return
from .models import Song, Album, Author, Genre, UserSongPlay
from relations import RelatedFieldOptimized


class AuthorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'title', 'picture']


class AlbumReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['id', 'title', 'picture']


class SongReadSerializer(serializers.ModelSerializer):
    authors = AuthorReadSerializer(read_only=True, many=True)
    album = AlbumReadSerializer(read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'picture', 'audio', 'authors', 'album']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.context.get('album', True):
            data.pop('album')
        if not self.context.get('authors', True):
            data.pop('authors')
        return data


class AuthorSerializer(serializers.ModelSerializer):
    # change title, picture
    albums = AlbumReadSerializer(many=True, read_only=True)
    # songs = SongReadSerializer(many=True, read_only=True, context=get_dict(album=True))
    picture = serializers.ImageField(required=False)

    class Meta:
        model = Author
        fields = ['id', 'title', 'picture', 'albums']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        author = Author(title=validated_data['title'], user=self.context.get('request').user)
        author.picture = validated_data.get('picture', author.picture)
        author.save()

        return author

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        return instance


class AlbumSerializer(serializers.ModelSerializer):
    # change title, picture, author
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    picture = serializers.ImageField(required=False)

    # songs = SongReadSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'author', 'picture']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        author = validate_exist_and_return(author_data, Author)

        album = Album(title=validated_data['title'], user=self.context.get('request').user)
        album.picture = validated_data.get('picture', album.picture)
        album.author = author
        album.save()

        return album

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', None)
        authors = validate_exist_and_return_array(authors_data, Author)
        instance.authors.add(*authors)

        instance.title = validated_data.get('title', instance.title)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']
        read_only_fields = ['id']


class SongSerializer(serializers.ModelSerializer):
    # change title, picture, album, genres, author
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    picture = serializers.ImageField(required=False)

    class Meta:
        model = Song
        fields = ['id', 'title', 'audio', 'picture', 'genres', 'album', 'authors', 'user']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        album_data = validated_data.pop('album', None)
        album = validate_exist_and_return(album_data, Album)
        genres_data = validated_data.pop('genres', None)
        genres = validate_exist_and_return_array(genres_data, Genre)
        authors_data = validated_data.pop('authors', None)
        authors = validate_exist_and_return_array(authors_data, Author)

        song = Song(title=validated_data['title'], user=self.context.get('request').user,
                    audio=validated_data['audio'])
        song.picture = validated_data['picture']
        song.album = album
        song.save()

        song.genres.add(*genres)
        song.authors.add(*authors)
        song.save()

        return song

    def update(self, instance, validated_data):
        album_data = validated_data.pop('album', None)
        album = validate_exist_and_return(album_data, Album)
        genres_data = validated_data.pop('genres', None)
        genres = validate_exist_and_return_array(genres_data, Genre)
        authors_data = validated_data.pop('authors', None)
        authors = validate_exist_and_return_array(authors_data, Author)

        instance.title = validated_data.get('title', instance.title)
        instance.picture = validated_data.get('picture', instance.picture)
        if album is not None:
            instance.album = album
        instance.genres.add(*genres)
        instance.authors.add(*authors)
        instance.save()

        return instance


class UserSongPlaySerializer(serializers.ModelSerializer):
    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())

    class Meta:
        model = UserSongPlay
        fields = ['song', 'user', 'count']
        read_only_fields = ['user']

    def create(self, validated_data):
        song_id = validated_data.pop('song', None)
        song = validate_exist_and_return(song_id, Song)
        user = self.context.get('request').user

        try:
            play = UserSongPlay.objects.get(user=user, song=song)
        except UserSongPlay.DoesNotExist:
            play = UserSongPlay(user=user, song=song)

        play.count += 1
        play.save()

        return play
