# Generated by Django 5.0.4 on 2024-05-06 19:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0025_rename_play_usersongplay'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='users_plays',
            field=models.ManyToManyField(blank=True, related_name='songs_user_played', through='library.UserSongPlay', to=settings.AUTH_USER_MODEL),
        ),
    ]