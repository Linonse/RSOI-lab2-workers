import uuid
from TestUtils.models import BaseTestCase
from StoriesApp.models import Storie


class AllStoriesTestCase(BaseTestCase):
    """
    Тест для получения списка всех историй
    """
    def setUp(self):
        super().setUp()
        self.storie1, _ = Storie.objects.get_or_create(
            from_user_id=1,
            to_user_id=2,
            text='Text',
			back=3
        )
        self.storie2, _ = Storie.objects.get_or_create(
            from_user_id=2,
            to_user_id=3,
			text='Text2',
            back=4
        )
        self.url_404 = self.url_prefix + 'stories/?user_id=0'
        self.url_200 = self.url_prefix + f'stories/?user_id={self.storie1.to_user_id}'

    def testGet404(self):
        strs = self.get_response_and_check_status(url=self.url_404, expected_status_code=200)
        self.assertEqual(len(strs), 0)


    def testGet200(self):
        response = self.get_response_and_check_status(url=self.url_200)
        self.assertEqual(len(response), 2)


class ConcreteStorieTestCase(BaseTestCase):
    """
    Тесты для ендпоинта api/stories/<storie:id>/
    """
    def setUp(self):
        super().setUp()
        self.storie1, _ = Storie.objects.get_or_create(
            from_user_id=1,
            to_user_id=2,
            text='Text',
			back=3
        )
        self.storie2, _ = Storie.objects.get_or_create(
            from_user_id=2,
            to_user_id=3,
            text='Text2',
			back=4
        )
        uuid_404 = uuid.uuid4()
        while uuid_404 in (self.storie1.uuid, self.storie2.uuid):
            uuid_404 = uuid.uuid4()
        self.url_404 = self.url_prefix + f'stories/{str(uuid_404)}/'
        self.url_200 = self.url_prefix + f'stories/{self.storie1.uuid}/'

    def testGet404(self):
        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet200(self):
        response = self.get_response_and_check_status(url=self.url_200)
        self.assertEqual(response['uuid'], str(self.storie1.uuid))

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete204(self):
        _ = self.delete_response_and_check_status(url=self.url_200, expected_status_code=204)
