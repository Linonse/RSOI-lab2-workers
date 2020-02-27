import uuid
from django.db import models
EMOJI = [(1, 'smile'),
         (2, 'neutral'),
		 (3, 'sad'),
		 (4, 'tears-of-joy'),
		 (5, 'upside-down'),
		 (6, 'loudly-crying'),
		 (7, 'smile-sweat'),
		 (8, 'winking-eye'),
		 (9, 'sad-sweat')]


class Sticker(models.Model):
    """
    Модель стикера
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, null=False)
    width = models.IntegerField()
    height = models.IntegerField()
    emotion = models.IntegerField(choices=EMOJI, null=False)

    @property
    def extension(self):
        return self.name.split('.')[-1]

    @property
    def sticker_size(self):
        return f'{self.width}x{self.height}'

    def __str__(self):
        return self.name
