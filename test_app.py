import unittest

from sitemap_generator import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_generator(self):
        data = {
            'url': 'http://test.com',
            'depth':  '1',
            'format': 'screen'
        }
        response = self.app.post('/generator', json=data)
        self.assertEqual(response.status_code, 200)

