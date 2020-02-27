from rest_framework import status
from rest_framework.views import Response, Request, APIView
from rest_framework.generics import ListCreateAPIView
from MusicApp.serializers import MusicSerializer
from MusicApp.models import Music


class MusicsView(ListCreateAPIView):
    """
    Вьюха для списка музыки
    """
    serializer_class = MusicSerializer

    def get_queryset(self):
        return Music.objects.all()


class ConcreteMusicView(APIView):
    """
    Вьюха для конкретного музыкального файла
    """
    def get(self, request: Request, music_uuid):
        try:
            music = Music.objects.get(pk=music_uuid)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MusicSerializer(instance=music)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, music_uuid):
        try:
            music = Music.objects.get(pk=music_uuid)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MusicSerializer(instance=music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, music_uuid):
        try:
            music = Music.objects.get(pk=music_uuid)
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
