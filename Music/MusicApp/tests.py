import uuid
from TestUtils.models import BaseTestCase
from MusicApp.models import Music


class MusicsViewTestCase(BaseTestCase):
    """
    Тесты для ендпоинта /api/music/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'music/'
        self.music1, _ = Music.objects.get_or_create(name='test1', length=60)
        self.music2, _ = Music.objects.get_or_create(name='test2', length=120)
        self.data_400 = {
            'na': 'no',
        }
        self.data_201 = {
            'name': 'post',
            'length': 180,
        }

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url)
        # Количество объектов в ответе
        self.assertEqual(len(response), 2)
        # UUID
        self.assertEqual(response[0]['uuid'], str(self.music1.uuid))
        self.assertEqual(response[1]['uuid'], str(self.music2.uuid))
        # Правильность остальных данных
        self.assertEqual(response[0]['name'], self.music1.name)
        self.assertEqual(response[1]['name'], self.music2.name)
        self.assertEqual(response[0]['length'], self.music1.length)
        self.assertEqual(response[1]['length'], self.music2.length)

    def testPost400(self):
        _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)

    def testPost(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            new = Music.objects.get(pk=response['uuid'])
        except Music.DoesNotExist:
            self.assertTrue(False)
            return  # Чтобы идеха не подсвечивала new желтым ниже
        self.assertEqual(new.name, self.data_201['name'])
        self.assertEqual(new.length, self.data_201['length'])


class ConcreteMusicViewTestCase(BaseTestCase):
    """
    Тесты для ендпоинта /api/music/<music_uuid>/
    """
    def setUp(self):
        super().setUp()
        self.music, _ = Music.objects.get_or_create(name='test', length=60)
        uuid_tmp = uuid.uuid4()
        self.url = self.url_prefix + f'music/{str(self.music.uuid)}/'
        self.url_404 = self.url_prefix + f'music/{uuid_tmp}/'
        while uuid_tmp == str(self.music.uuid):
            uuid_tmp = uuid.uuid4()
            self.url_404 = self.url_prefix + f'music/{uuid_tmp}/'

    def testGet404(self):
        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url, expected_status_code=200)
        self.assertEqual(response['uuid'], str(self.music.uuid))
        self.assertEqual(response['name'], self.music.name)
        self.assertEqual(response['length'], self.music.length)

    def testDelete(self):
        _ = self.delete_response_and_check_status(url=self.url, expected_status_code=204)
        self.assertEqual(Music.objects.count(), 0)
