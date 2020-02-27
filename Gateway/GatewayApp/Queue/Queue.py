from typing import Union


class Queue:
    MUSIC, STICKER = 'music', 'sticker'
    _music_status, _sticker_status = 1, 1
    queue = []

    @staticmethod
    def _add_task_to_queue(request, data, uuid, ttype):
        Queue.queue.append({
            'request': request,
            'data': data,
            'uuid': uuid,
            'type': ttype,
        })

    @staticmethod
    def add_sticker_task(request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        Queue._sticker_status = 0
        Queue._add_task_to_queue(request, data, uuid, ttype=Queue.STICKER)
        print('Add sticker task to queue')

    @staticmethod
    def add_music_task(request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        Queue._music_status = 0
        Queue._add_task_to_queue(request, data, uuid, ttype=Queue.MUSIC)
        print('Add music task to queue')

    @staticmethod
    def fire_music_tasks():
        from GatewayApp.requesters.music_requester import MusicRequester
        if Queue._music_status == 1:
            return
        else:
            Queue._music_status = 1
        print('Firing music tasks...')
        atasks = list(filter(lambda x: x['type'] == Queue.MUSIC, Queue.queue))
        ar = MusicRequester()
        tasks_to_delete = []
        for task in atasks:
            if task['request'].method == 'POST':
                _, code = ar.post_music(task['request'], task['data'])
            elif task['request'].method == 'PATCH':
                _, code = ar.patch_music(task['request'], task['uuid'], task['data'])
            elif task['request'].method == 'DELETE':
                _, code = ar.delete_music(task['request'], task['uuid'])
            else:
                code = 501
            if code < 500:
                tasks_to_delete.append(task)
        for task in tasks_to_delete:
            Queue.queue.remove(task)
        print(f'{len(tasks_to_delete)} music tasks fired with success')

    @staticmethod
    def fire_sticker_tasks():
        from GatewayApp.requesters.stickers_requester import StickersRequester
        if Queue._sticker_status == 1:
            return
        else:
            Queue._sticker_status = 1
        print('Firing sticker tasks...')
        itasks = list(filter(lambda x: x['type'] == Queue.STICKER, Queue.queue))
        ir = StickersRequester()
        tasks_to_delete = []
        for task in itasks:
            if task['request'].method == 'POST':
                _, code = ir.post_sticker(task['request'], task['data'])
            elif task['request'].method == 'PATCH':
                _, code = ir.patch_sticker(task['request'], task['uuid'], task['data'])
            elif task['request'].method == 'DELETE':
                _, code = ir.delete_sticker(task['request'], task['uuid'])
            else:
                code = 501
            if code < 500:
                tasks_to_delete.append(task)
        for task in tasks_to_delete:
            Queue.queue.remove(task)
        print(f'{len(tasks_to_delete)} image tasks fired with success')
