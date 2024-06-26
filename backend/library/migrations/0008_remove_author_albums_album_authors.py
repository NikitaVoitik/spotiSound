# Generated by Django 5.0.4 on 2024-05-02 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_author_albums'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='albums',
        ),
        migrations.AddField(
            model_name='album',
            name='authors',
            field=models.ManyToManyField(related_name='album_authors', to='library.author'),
        ),
    ]
