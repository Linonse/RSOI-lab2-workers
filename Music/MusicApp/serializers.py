from rest_framework import serializers
from MusicApp.models import Music


class MusicSerializer(serializers.ModelSerializer):
    """
    Сериализатор музыки
    """
    class Meta:
        model = Music
        fields = [
            'uuid',
            'name',
            'length',
        ]

    def create(self, validated_data):
        new = Music.objects.create(**validated_data)
        return new

    def update(self, instance: Music, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.length = validated_data.get('length', instance.length)
        instance.save()
        return instance
