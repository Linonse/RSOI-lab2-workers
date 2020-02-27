from rest_framework import serializers
from StickersApp.models import Sticker


class StickerSerializer(serializers.ModelSerializer):
    """
    Сериализатор стикера
    """
    class Meta:
        model = Sticker
        fields = [
            'uuid',
            'name',
            'extension',
            'sticker_size',
            'width',
            'height',
			'emotion'
        ]
        extra_kwargs = {
            'width': {'write_only': True},
            'height': {'write_only': True},
        }

    def create(self, validated_data):
        new_sticker = Sticker.objects.create(**validated_data)
        return new_sticker

    def update(self, instance: Sticker, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.emotion = validated_data.get('emotion', instance.emotion)
        instance.save()
        return instance
