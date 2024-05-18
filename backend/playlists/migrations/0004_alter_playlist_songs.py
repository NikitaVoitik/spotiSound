# Generated by Django 5.0.4 on 2024-05-08 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0026_alter_song_users_plays'),
        ('playlists', '0003_alter_playlist_songs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(blank=True, through='playlists.SongPlaylist', to='library.song'),
        ),
    ]