from rest_framework import serializers
from StoriesApp.models import Storie


class StorieSerializer(serializers.ModelSerializer):
    """
    Сериалиатор истории
    """
    class Meta:
        model = Storie
        fields = [
            'uuid',
            'from_user_id',
            'to_user_id',
            'text',
            'sticker_uuid',
            'music_uuid',
			'back',
        ]

    def create(self, validated_data):
        new = Storie.objects.create(**validated_data)
        return new

    def update(self, instance: Storie, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.sticker_uuid = validated_data.get('sticker_uuid', instance.sticker_uuid)
        instance.music_uuid = validated_data.get('music_uuid', instance.music_uuid)
        instance.back = validated_data.get('back', instance.back)
        instance.save()
        return instance
