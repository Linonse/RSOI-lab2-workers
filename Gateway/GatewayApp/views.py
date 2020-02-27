from rest_framework.views import Response, Request, APIView
from GatewayApp.requesters.stories_requester import StoriesRequester
from GatewayApp.requesters.stickers_requester import StickersRequester
from GatewayApp.requesters.music_requester import MusicRequester
from GatewayApp.requesters.auth_requester import AuthRequester
from GatewayApp.permissions import IsAuthenticatedThroughAuthService
from django.shortcuts import render
from django.contrib.auth import authenticate
from django import forms
#from .forms import StorieForm

def main(request):
    return render(request, 'api/main.html')
'''
user = authenticate(username='john', password='secret')
if user is not None:
    # the password verified for the user
    if user.is_active:
        print("User is valid, active and authenticated")
    else:
        print("The password is valid, but the account has been disabled!")
else:
    # the authentication system was unable to verify the username and password
    print("The username and password were incorrect.")

## Функция представления registration
#
# Регистрация новых пользователей
# \return Страницу с формой для авторизации
def auth(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                if user.is_active:
                    return HttpResponseRedirect('/api/main.html')
                else:
                    return HttpResponseRedirect('/api/main.html')
            else:
                return HttpResponseRedirect('/api/main.html')
    else:
        form = UserForm()
        return render(request, 'api/auth.html', {'form': form})
'''

# MARK: - Auth
class BaseAuthView(APIView):
    REQUESTER = AuthRequester()

class AuthView(BaseAuthView):
    """
    Получение токена по юзернейму и паролю
    """
    def post(self, request: Request):
        response_json, code = self.REQUESTER.authenticate(data=request.data)
        return Response(response_json, status=code)

class RegisterView(BaseAuthView):
    """
    Регистрация
    """
    def post(self, request: Request):
        response_json, code = self.REQUESTER.register(request=request, data=request.data)
        return Response(data=response_json, status=code)


class GetUserInfoView(BaseAuthView):
    """
    Получение инфы о юзере по токену
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request):
        response_json, code = self.REQUESTER.get_user_info(request=request)
        return Response(response_json, status=code)

    def delete(self, request: Request):
        response_json, code = self.REQUESTER.delete_user(request=request)
        return Response(response_json, status=code)


class UsersView(BaseAuthView):
    """
    Получение списка юзеров
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request):
        response_json, code = self.REQUESTER.get_users(request=request)
        return Response(response_json, status=code)


class ConcreteUserView(BaseAuthView):
    """
    Получение конкретного пользователя
    """
    permission_classes = (IsAuthenticatedThroughAuthService,)

    def get(self, request: Request, user_id):
        response_json, code = self.REQUESTER.get_concrete_user(request=request, user_id=user_id)
        return Response(response_json, status=code)


# MARK: - Музыка
class BaseMusicView(APIView):
    REQUESTER = MusicRequester()


class MusicsView(BaseMusicView):
    """
    Получение всей музыки
    """
    #permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = self.REQUESTER.get_musics(request=request)
        if code == 200:
            return render(request, 'api/music_list.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})

    def post(self, request: Request):
        data, code = self.REQUESTER.post_music(request=request, data=request.data)
        if code == 200:
            return render(request, 'api/music_list.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})
        #return Response(data, status=code)

class ConcreteMusicView(BaseMusicView):
    """
    Получение определенного музыкального файла
    """
    #permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, music_uuid):
        data, code = self.REQUESTER.get_concrete_music(request=request, uuid=music_uuid)
        if code == 200:
            return render(request, 'api/music_info.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})

    def patch(self, request: Request, music_uuid):
        data, code = self.REQUESTER.patch_music(request=request, uuid=music_uuid, data=request.data)
        if code == 200:
            return render(request, 'api/music_info.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})

    def delete(self, request: Request, music_uuid):
        data, code = self.REQUESTER.delete_music(request=request, uuid=music_uuid)
        if code == 200:
            return render(request, 'api/music_info.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})


# MARK: - Стикеры
class BaseStickerView(APIView):
    REQUESTER = StickersRequester()


class StickersView(BaseStickerView):
    """
    Получение всех стикеров
    """
    #permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = self.REQUESTER.get_stickers(request=request)
        if code == 200:
            return render(request, 'api/stickers_list.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})

    def post(self, request: Request):
        data, code = self.REQUESTER.post_sticker(request=request, data=request.data)
        if code == 200:
            return render(request, 'api/stickers_list.html', {'data': data, 'status': code})
        else:
            return render(request, 'api/errorr.html', {'status': code})


class ConcreteStickerView(BaseStickerView):
    """
    Получение определеного стикера
    """
    #permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, sticker_uuid):
        data, code = self.REQUESTER.get_concrete_sticker(request=request, uuid=sticker_uuid)
        return render(request, 'api/sticker_info.html', {'data': data, 'status': code})

    def patch(self, request: Request, sticker_uuid):
        data, code = self.REQUESTER.patch_sticker(request=request, uuid=sticker_uuid, data=request.data)
        return render(request, 'api/sticker_info.html', {'data': data, 'status': code})

    def delete(self, request: Request, sticker_uuid):
        data, code = self.REQUESTER.delete_sticker(request=request, uuid=sticker_uuid)
        return render(request, 'api/sticker_info.html', {'data': data, 'status': code})


# MARK: - Истории
class BaseStorieView(APIView):
    REQUESTER = StoriesRequester()


class StoriesView(BaseStorieView):
    """
    Получение всех историй
    """
    #permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request):
        data, code = self.REQUESTER.get_stories(request=request)
        return render(request, 'api/stories_list.html', {'data': data, 'status': code})

    def post(self, request: Request):
        data, code = self.REQUESTER.post_storie(request=request, data=request.data)
        return render(request, 'api/stories_list.html', {'data': data, 'status': code})
'''
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
            return redirect('main')
    else:
        form = StorieForm()
    return render(request, 'api/storie_form.html', {'form': form})
'''

class ConcreteStorieView(BaseStorieView):
    """
    Получение определеной истории
    """
    #permission_classes = (IsAuthenticatedThroughAuthService, )

    def get(self, request: Request, storie_uuid):
        data, code = self.REQUESTER.get_concrete_storie(request=request, uuid=storie_uuid)
        return render(request, 'api/storie_info.html', {'data': data, 'status': code})

    def patch(self, request: Request, storie_uuid):
        data, code = self.REQUESTER.patch_storie(request=request, uuid=storie_uuid, data=request.data)
        return render(request, 'api/storie_info.html', {'data': data, 'status': code})

    def delete(self, request: Request, storie_uuid):
        data, code = self.REQUESTER.delete_storie(request=request, uuid=storie_uuid)
        return render(request, 'api/storie_info.html', {'data': data, 'status': code})
