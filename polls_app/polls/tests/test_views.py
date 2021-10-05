from django.test import TestCase

class HomePageTest(TestCase):

    def test_root_returns_http_response(self):
        response = self.client.get('/polls/')
        self.assertIn("Hello, world. You're at the polls index.", str(response.content))

