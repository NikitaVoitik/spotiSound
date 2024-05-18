from rest_framework import serializers, fields
from .models import Playlist, Collection
from library.serializers import SongReadSerializer
from library.models import Song
from utils import validate_exist_and_return_array, validate_exist_and_return
from relations import RelatedFieldOptimized


class CollectionSerializer(serializers.ModelSerializer):
    songs = SongReadSerializer(many=True, read_only=True)
    picture = fields.ImageField(required=False)

    class Meta:
        model = Collection
        fields = ['id', 'picture', 'user', 'songs']
        read_only_fields = ['user', 'id']

    def create(self, validated_data):
        if validated_data.get('songs') is not None:
            validated_data.pop('songs')
        playlist = Collection.objects.create(**validated_data)
        return playlist

    def update(self, instance, validated_data):
        if validated_data.get('songs') is not None:
            validated_data.pop('songs')
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        return instance


class PlaylistSerializer(CollectionSerializer):
    songs = SongReadSerializer(many=True, read_only=True)
    picture = fields.ImageField(required=False)

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'picture', 'user', 'songs']
        read_only_fields = ['user', 'id']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        if validated_data.get('songs') is not None:
            validated_data.pop('songs')
        playlist = Playlist.objects.create(**validated_data)
        return playlist

    def update(self, instance, validated_data):
        if validated_data.get('songs') is not None:
            validated_data.pop('songs')
        instance.title = validated_data.get('title', instance.title)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        return instance
