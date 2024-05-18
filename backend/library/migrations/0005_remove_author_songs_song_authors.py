# Generated by Django 5.0.4 on 2024-05-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_album_user_alter_author_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='library',
        ),
        migrations.AddField(
            model_name='song',
            name='authors',
            field=models.ManyToManyField(related_name='author_songs', to='library.author'),
        ),
    ]
