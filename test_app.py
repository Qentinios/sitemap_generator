import json
import unittest

from sitemap_generator import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_generator(self):
        data = {
            'url': 'http://lol.com',
            'depth':  '1',
            'format': 'screen'
        }
        response = self.app.post('/', json=data)
        self.assertEqual(response.status_code, 200)

        self.assertNotEqual(response.data.decode("utf-8"), "{}\n"),

