from django.db import models

# Create your models here.

import uuid
from django.db import models


class Storie(models.Model):
    """
    Модель истории
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user_id = models.IntegerField(null=False)
    to_user_id = models.IntegerField(null=False)
    text = models.CharField(null=True, max_length=300)
    sticker_uuid = models.UUIDField(null=True, blank=True)
    music_uuid = models.UUIDField(null=True, blank=True)
    back = models.IntegerField(choices=[(1, 'white'), (2, 'red'), (3, 'yellow'), (4, 'green'), (5, 'black')], null=False)

    def __str__(self):
        return f'Storie, uuid={self.uuid}'

