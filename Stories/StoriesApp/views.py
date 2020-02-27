from rest_framework import status
from rest_framework.views import APIView, Response, Request
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q
from StoriesApp.serializers import StorieSerializer
from StoriesApp.models import Storie
from django import forms
from .forms import StorieForm
from django.shortcuts import render, redirect

def done(request):
    return render(request, 'api/done.html')
def nope(request):
    return render(request, 'api/nope.html')
## Функция представления new_book
#
# Добавление книги
# \return Страницу с сообщением
def new_storie(request):
    if request.method == "POST":
        form = StorieForm(request.POST)
        if form.is_valid():
            storie = form.save(commit=False)
            storie.save()
            try:
                msg = Storie.objects.get(pk=storie.uuid)
            except Storie.DoesNotExist:
                return redirect('nope')
            #проверка что всё сохранилось
            return redirect('done')
        return render(request, 'api/storie_form.html', {'form': form})
    else:
        form = StorieForm()
    return render(request, 'api/storie_form.html', {'form': form})

class AllStoriesView(ListCreateAPIView):
    """
    Вьюха для вывода всех историй и добавления новой
    """
    serializer_class = StorieSerializer

    def get_queryset(self):
        request = self.request
        try:
            user_id = request.query_params['user_id']
        except KeyError:
            return Response({'error': 'Wrong query params'}, status=status.HTTP_400_BAD_REQUEST)
        strs = Storie.objects.filter(Q(from_user_id=user_id) | Q(to_user_id=user_id))
        return strs

    # def post(self, request: Request):
    #     serializer = StorieSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConcreteStorieView(APIView):
    """
    Вьюха для отображения конкретной истории
    """
    def get(self, request: Request, storie_uuid):
        try:
            msg = Storie.objects.get(pk=storie_uuid)
        except Storie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StorieSerializer(instance=msg)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, storie_uuid):
        try:
            msg = Storie.objects.get(pk=storie_uuid)
        except Storie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StorieSerializer(instance=msg, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, storie_uuid):
        try:
            msg = Storie.objects.get(pk=storie_uuid)
        except Storie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
