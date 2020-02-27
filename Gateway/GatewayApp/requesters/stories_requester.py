from typing import Tuple, Union
from GatewayApp.requesters.requester import Requester


class StickerGetError(Exception):
    def __init__(self, code: int, err_json: dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class MusicGetError(Exception):
    def __init__(self, code: int, err_json: dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class UserGetError(Exception):
    def __init__(self, code: int, err_json: dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class StoriesRequester(Requester):
    HOST = Requester.BASE_HOST + ':8002/api/stories/'

    # MARK: - Privates, getiing sticker and music
    def __get_and_set_storie_sticker(self, storie: dict) -> dict:
        from GatewayApp.requesters.stickers_requester import StickersRequester
        sticker_uuid = storie['sticker_uuid']  # Можеть быть кей еррор, поймаем в гет_сторис
        if sticker_uuid is not None:
            sticker_json, sticker_status = StickersRequester().get_concrete_sticker(request=None, uuid=sticker_uuid)
            if sticker_status != 200:
                from Gateway.settings import DEBUG
                if DEBUG:
                    print(sticker_json)
                raise StickerGetError(code=sticker_status, err_json=sticker_json)
            storie['sticker'] = sticker_json
        return storie

    def __get_and_set_storie_music(self, storie: dict) -> dict:
        from GatewayApp.requesters.music_requester import MusicRequester
        music_uuid = storie['music_uuid']  # Можеть быть кей еррор, поймаем в гет_сторис
        if music_uuid is not None:
            music_json, music_status = MusicRequester().get_concrete_music(request=None, uuid=music_uuid)
            if music_status != 200:
                from Gateway.settings import DEBUG
                if DEBUG:
                    print(music_json)
                raise MusicGetError(code=music_status, err_json=music_json)
            storie['music'] = music_json
        return storie

    def __get_and_set_storie_attachments(self, storie: dict) -> dict:
        try:
            storie = self.__get_and_set_storie_music(storie)
        except MusicGetError:
            storie['music'] = None
        try:
            storie = self.__get_and_set_storie_sticker(storie)
        except StickerGetError:
            storie['sticker'] = None
        return storie

    def __get_and_set_user_from(self, request, storie: dict) -> dict:
        from GatewayApp.requesters.auth_requester import AuthRequester
        user_id = storie['to_user_id']
        if user_id is not None:
            user_json, user_status = AuthRequester().get_concrete_user(request=request, user_id=user_id)
            if user_status != 200:
                raise UserGetError(code=user_status, err_json=user_json)
            storie['to_user'] = user_json
        return storie

    def __get_and_set_user_to(self, request, storie: dict) -> dict:
        from GatewayApp.requesters.auth_requester import AuthRequester
        user_id = storie['from_user_id']
        if user_id is not None:
            user_json, user_status = AuthRequester().get_concrete_user(request=request, user_id=user_id)
            if user_status != 200:
                raise UserGetError(code=user_status, err_json=user_json)
            storie['from_user'] = user_json
        return storie

    def __get_and_set_storie_users(self, request, storie: dict) -> dict:
        storie = self.__get_and_set_user_from(request, storie)
        storie = self.__get_and_set_user_to(request, storie)
        return storie

    def get_stories(self, request) -> Tuple[dict, int]:
        host = self.HOST
        # User info
        user_json, code = self._get_user_by_token(request)
        if code != 200:
            return user_json, code
        host += f'?user_id={user_json["id"]}'
        # Limit-offset
        l_o = self.get_limit_offset_from_request(request)
        if l_o is not None:
            host += f'&limit={l_o[0]}&offset={l_o[1]}'
        response = self.perform_get_request(host)
        if response is None:
            return self.ERROR_RETURN
        response_json = self.next_and_prev_links_to_params(self.get_valid_json_from_response(response))
        # Adding users
        if isinstance(response_json, dict):
            actual_stories = response_json['results']
            for i in range(len(actual_stories)):
                actual_stories[i] = self.__get_and_set_storie_users(request, actual_stories[i])
            response_json['results'] = actual_stories
        else:
            for i in range(len(response_json)):
                response_json[i] = self.__get_and_set_storie_users(request, response_json[i])
        return response_json, response.status_code

    def get_concrete_storie(self, request, uuid: str) -> Tuple[dict, int]:
        response = self.perform_get_request(self.HOST + uuid + '/')
        if response is None:
            return self.ERROR_RETURN
        if response.status_code != 200:
            return self.get_valid_json_from_response(response), response.status_code
        valid_json = self.get_valid_json_from_response(response)
        try:
            ans = self.__get_and_set_storie_attachments(valid_json)
            ans = self.__get_and_set_storie_users(request, ans)
        except KeyError:
            return {'error': 'Key error was raised, no sticker or music uuid in storie json!'}, 500
        except UserGetError as e:
            return e.err_msg, e.code
        return ans, 200

    def _check_if_sticker_exists(self, sticker_uuid) -> bool:
        from GatewayApp.requesters.stickers_requester import StickersRequester
        _, code = StickersRequester().get_concrete_sticker(request=None, uuid=sticker_uuid)
        return code == 200

    def _check_if_music_exists(self, music_uuid) -> bool:
        from GatewayApp.requesters.music_requester import MusicRequester
        _, code = MusicRequester().get_concrete_music(request=None, uuid=music_uuid)
        return code == 200

    def _check_if_user_exists(self, request, user_id) -> bool:
        from GatewayApp.requesters.auth_requester import AuthRequester
        _, code = AuthRequester().get_concrete_user(request=request, user_id=user_id)
        return code == 200

    def _get_user_by_token(self, request) -> Tuple[dict, int]:
        from GatewayApp.requesters.auth_requester import AuthRequester
        user_json, code = AuthRequester().get_user_info(request)
        return user_json, code

    def _check_if_attachments_exist(self, request, data: dict) -> Tuple[dict, int]:
        # Есть ли такой стикер
        try:
            if data['sticker_uuid']:
                if not self._check_if_sticker_exists(data['sticker_uuid']):
                    return {'error': f'Sticker with uuid "{data["sticker_uuid"]}" does not exist!'}, 404
        except KeyError:
            pass
        # Есть ли такая музыка
        try:
            if data['music_uuid']:
                if not self._check_if_music_exists(data['music_uuid']):
                    return {'error': f'Music with uuid "{data["music_uuid"]}" does not exist!'}, 404
        except KeyError:
            pass
        # Есть ли такие юзеры
        try:
            if data['to_user_id']:
                if not self._check_if_user_exists(request, data['to_user_id']):
                    return {'error': f'User with id "{data["to_user_id"]}" does not exist!'}, 404
        except KeyError:
            pass
        return {}, 200

    def _add_from_user_id_to_data(self, request, data: dict) -> Tuple[dict, int]:
        # Получение айдишника юзера, который пишет
        user_json, code = self._get_user_by_token(request)
        if code != 200:
            return user_json, code
        data['from_user_id'] = user_json['id']
        return data, 200

    def __music_rollback(self, request, data: dict):
        from GatewayApp.requesters.audio_requester import MusicRequester
        try:
            MusicRequester().delete_audio(request, data['music_uuid'])
        except KeyError:
            pass

    def __sticker_rollback(self, request, data: dict):
        from GatewayApp.requesters.stickers_requester import StickersRequester
        try:
            StickersRequester().delete_sticker(request, data['sticker_uuid'])
        except KeyError:
            pass

    def __attachments_rollback(self, request, data: dict):
        self.__sticker_rollback(request, data)
        self.__music_rollback(request, data)

    def post_storie(self, request, data: dict) -> Tuple[dict, int]:
        from GatewayApp.requesters.music_requester import MusicRequester
        from GatewayApp.requesters.stickers_requester import StickersRequester
        # check_json, code = self._check_if_attachments_exist(request, data)
        # Прикрепление юзера и проверка что он вообще есть
        try:
            if not self._check_if_user_exists(request, data['to_user_id']):
                return {'error': 'No user found with given id'}, 404
        except KeyError:
            return {'error': 'No to_user_id key was given'}, 400
        data, code = self._add_from_user_id_to_data(request, data)
        if code != 200:
            return data, code
        # ПОСТ музыки
        try:
            upload_json, code = MusicRequester().post_music(request, data['music'])
            if code != 201:
                return upload_json, code
            data['music_uuid'] = upload_json['uuid']
        except KeyError:
            pass
        # ПОСТ стикера
        try:
            upload_json, code = StickersRequester().post_sticker(request, data['sticker'])
            if code != 201:
                self.__music_rollback(request, data)  # Rollback если в посте стикера ошибка
                return upload_json, code
            data['sticker_uuid'] = upload_json['uuid']
        except KeyError:
            pass
        # Пост самой сторис
        response = self.perform_post_request(self.HOST, data=data)
        if response is None:
            self.__attachments_rollback(request, data)
            return Requester.ERROR_RETURN
        resp_json = self.get_valid_json_from_response(response)
        if response.status_code != 201:
            self.__attachments_rollback(request, data)
            return resp_json, response.status_code
        try:
            resp_json = self.__get_and_set_storie_users(request, resp_json)
        except KeyError:
            return {'error': 'Key error was raised while getting user json!'}, 500
        except UserGetError as e:
            return e.err_msg, e.code
        return resp_json, response.status_code

    def patch_storie(self, request, uuid: str, data: dict) -> Tuple[dict, int]:
        check_json, code = self._check_if_attachments_exist(request, data)
        if code != 200:
            return check_json, code
        try:
            if not self._check_if_user_exists(request, data['to_user_id']):
                return {'error': 'No user found with given id'}, 404
        except KeyError:
            return {'error': 'No to_user_id key was given'}, 400
        data, code = self._add_from_user_id_to_data(request, data)
        if code != 200:
            return data, code
        response = self.perform_patch_request(self.HOST + f'{uuid}/', data=data)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def _delete_sticker_from_storie(self, request, storie_json: dict) -> Tuple[dict, int]:
        from GatewayApp.requesters.stickers_requester import StickersRequester
        if storie_json['sticker_uuid']:
            del_json, code = StickersRequester().delete_sticker(request, storie_json['sticker_uuid'])
            if code not in (204, 404):
                return del_json, code
        return {}, 204

    def _delete_music_from_storie(self, request, storie_json: dict) -> Tuple[dict, int]:
        from GatewayApp.requesters.music_requester import MusicRequester
        if storie_json['music_uuid']:
            del_json, code = MusicRequester().delete_music(request, storie_json['music_uuid'])
            if code not in (204, 404):
                return del_json, code
        return {}, 204

    def delete_storie(self, request, uuid: str) -> Tuple[dict, int]:
        storie_json, code = self.get_concrete_storie(request, uuid)
        if code != 200:
            return storie_json, code
        del_json, code = self._delete_sticker_from_storie(request, storie_json)
        if code != 204:
            return del_json, code
        del_json, code = self._delete_music_from_storie(request, storie_json)
        if code != 204:
            return del_json, code
        response = self.perform_delete_request(self.HOST + uuid)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code
