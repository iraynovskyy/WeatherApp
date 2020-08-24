from django.test import TestCase

class TestViews(TestCase):
    def test_index_view_anonymous(self):
        # self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')

    # def test_delete_view_anonymous(self):
    #     response = self.client.get('')
