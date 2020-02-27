# Generated by Django 2.2.5 on 2019-12-08 18:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sticker',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('emotion', models.IntegerField(choices=[(1, 'smile'), (1, 'neutral'), (1, 'sad'), (1, 'tears-of-joy'), (1, 'upside-down'), (1, 'loudly-crying'), (1, 'smile-sweat'), (1, 'winking-eye'), (1, 'sad-sweat')])),
            ],
        ),
    ]
