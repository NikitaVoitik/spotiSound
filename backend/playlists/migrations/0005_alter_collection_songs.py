# Generated by Django 5.0.4 on 2024-05-10 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0026_alter_song_users_plays'),
        ('playlists', '0004_alter_playlist_songs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='songs',
            field=models.ManyToManyField(related_name='collections', through='playlists.SongCollection', to='library.song'),
        ),
    ]
