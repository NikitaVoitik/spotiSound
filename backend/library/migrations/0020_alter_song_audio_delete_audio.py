# Generated by Django 5.0.4 on 2024-05-05 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0019_alter_song_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio',
            field=models.FileField(upload_to='tracks/'),
        ),
        migrations.DeleteModel(
            name='Audio',
        ),
    ]
