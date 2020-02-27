import uuid
from TestUtils.models import BaseTestCase
from StickersApp.models import Sticker


class StickersListTestCase(BaseTestCase):
    """
    Тест ендпоинта /api/stickers/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'stickers/'
        self.sticker1, _ = Sticker.objects.get_or_create(name='test1.jpg', width=300, height=300, emotion=1)
        self.sticker2, _ = Sticker.objects.get_or_create(name='test2.jpg.psd', width=100, height=100, emotion=2)
        self.data_400 = {
            'nam': 'no',
        }
        self.data_201 = {
            'name': 'post',
            'width': 300,
            'height': 300,
            'emotion': 3,
        }

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url)
        # Длинна массива
        self.assertEqual(len(response), 2)
        # UUID
        self.assertEqual(response[0]['uuid'], str(self.sticker1.uuid))
        self.assertEqual(response[1]['uuid'], str(self.sticker2.uuid))
        # Правильно рассчитывает расширение
        self.assertEqual(response[0]['extension'], 'jpg')
        self.assertEqual(response[1]['extension'], 'psd')
        # Правильно прислал расширение
        self.assertEqual(response[0]['extension'], self.sticker1.extension)
        self.assertEqual(response[1]['extension'], self.sticker2.extension)
        # Правильно выдает размер
        self.assertEqual(response[0]['sticker_size'], f'{self.sticker1.width}x{self.sticker1.height}')
        self.assertEqual(response[0]['emotion'], self.sticker1.emotion)
        self.assertEqual(response[1]['emotion'], self.sticker2.emotion)

    def testPost400(self):
        _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)

    def testPost201(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            new = Sticker.objects.get(pk=response['uuid'])
        except Sticker.DoesNotExist:
            self.assertTrue(False)
            return  # Чтобы идеха не выделяла new ниже желтым
        self.assertEqual(new.name, self.data_201['name'])
        self.assertEqual(new.width, self.data_201['width'])
        self.assertEqual(new.height, self.data_201['height'])
        self.assertEqual(new.emotion, self.data_201['emotion'])


class ConcreteStickerViewTestCase(BaseTestCase):
    """
    Тесты для ендпоинта /api/stickers/<sticker_uuid>/
    """
    def setUp(self):
        super().setUp()
        self.sticker, _ = Sticker.objects.get_or_create(name='test', width=300, height=300, emotion=3)
        uuid_tmp = uuid.uuid4()
        self.url_404 = self.url_prefix + f'stickers/{uuid_tmp}/'
        while uuid_tmp == self.sticker.uuid:
            uuid_tmp = uuid.uuid4()
            self.url_404 = self.url_prefix + f'stickers/{uuid_tmp}/'
        self.url = self.url_prefix + f'stickers/{self.sticker.uuid}/'

    def testGet404(self):
        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url, expected_status_code=200)
        self.assertEqual(response['uuid'], str(self.sticker.uuid))
        self.assertEqual(response['name'], self.sticker.name)
        self.assertEqual(response['sticker_size'], self.sticker.sticker_size)
        self.assertEqual(response['emotion'], self.sticker.emotion)

    def testDelete(self):
        _ = self.delete_response_and_check_status(url=self.url, expected_status_code=204)
        self.assertEqual(Sticker.objects.count(), 0)
