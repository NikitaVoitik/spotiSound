# Generated by Django 5.0.4 on 2024-05-04 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_alter_song_audio_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='audio_id',
            new_name='audio',
        ),
    ]