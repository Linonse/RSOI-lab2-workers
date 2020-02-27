from rest_framework import status
from rest_framework.views import Response, Request, APIView
from rest_framework.generics import ListCreateAPIView
from StickersApp.models import Sticker
from StickersApp.serializers import StickerSerializer


class StickersView(ListCreateAPIView):
    """
    Вьюха для списка стикеров
    """
    serializer_class = StickerSerializer

    def get_queryset(self):
        return Sticker.objects.all()


class ConcreteStickerView(APIView):
    """
    Вьюха для конкретного стикера
    """
    def get(self, request: Request, sticker_uuid):
        try:
            img = Sticker.objects.get(pk=sticker_uuid)
        except Sticker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StickerSerializer(instance=img)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, sticker_uuid):
        try:
            img = Sticker.objects.get(pk=sticker_uuid)
        except Sticker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StickerSerializer(instance=img, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, sticker_uuid):
        try:
            img = Sticker.objects.get(pk=sticker_uuid)
        except Sticker.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
