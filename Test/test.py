import requests

import os
import unittest


url = f"http://localhost:8000/"
file = 'test.pdf'


class TestServer(unittest.TestCase):
    """Тестирование функционала сервера"""
    headers = {'Content-type': 'pdf', 'Filename': file}

    def test_post_upload(self):
        """Тест на загрузку файла в сервис по адресу {url}/upload"""
        with open(os.path.join(os.getcwd(), file), 'rb') as f:
            data = f.read()
        response = requests.post(url + 'upload', data=data, headers=self.headers)
        response.text
        result = "{'status': 201, 'file is uploaded': 'test.pdf', \
'link for check': '0.0.0.0:8000/check/test.pdf', \
'link for download': '0.0.0.0:8000/download/test.pdf'}"
        self.assertEqual(201, response.status_code)
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_post_without_headers(self):
        """Тест на POST запрос без заголовков о загружаемом файле"""
        response = requests.post(url + 'upload')
        result = "{'status': 403, 'message': 'headers not found'}"
        self.assertEqual(403, response.status_code)
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_post_without_attach(self):
        """Тест на POST запрос без прикрепленного файла"""
        response = requests.post(url + 'upload', headers=self.headers)
        result = "{'status': 409, 'error': 'file not attached'}"
        self.assertEqual(409, response.status_code)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(result, response.content.decode('utf-8'))

    def test_post_bad_url(self):
        """Тест на POST запрос по неправильному адресу"""
        response = requests.post(url + 'uplodad', headers=self.headers)
        result = "{'status': 404, 'message': 'page not found'}"
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_post_root_url(self):
        """Тест на POST запрос по корневому адресу"""
        response = requests.post(url, headers=self.headers)
        result = "{'status': 404, 'message': 'page not found'}"
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_check_file(self):
        """Тест на GET запрос по адресу {url}/check для проверки наличия файла"""
        response = requests.get(url + 'check/' + file, headers=self.headers)
        result = "{'status': 200, 'file': 'test.pdf', 'message': 'is ready to download'}"
        self.assertEqual(200, response.status_code)
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_check_file_not_found(self):
        """Тест на GET запрос по адресу {url}/check/несуществующий файл"""
        response = requests.get(url + 'check/' + 'not_file', headers=self.headers)
        result = "{'status': 400, 'file': 'not_file', 'message': 'is not found'}"
        self.assertEqual(400, response.status_code)
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_check_url(self):
        """Тест на GET запрос по адресу {url}/check (без имени файла)"""
        response = requests.get(url + 'check/', headers=self.headers)
        result = "{'status': 404, 'message': 'page not found'}"
        self.assertEqual(404, response.status_code)
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_root_url(self):
        """Тест на GET запрос по корневому адресу"""
        response = requests.post(url, headers=self.headers)
        result = "{'status': 404, 'message': 'page not found'}"
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_file_not_found_download(self):
        """Тест на GET запрос по адресу {url}/download/несуществующий файл"""
        response = requests.get(url + 'download/' + 'not_file', headers=self.headers)
        result = "{'status': 400, 'file': 'not_file', 'message': 'is not found'}"
        self.assertEqual(400, response.status_code)
        self.assertEqual(result, response.content.decode('utf-8'))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_get_file(self):
        """Тест на загрузку файла"""
        response = requests.get(url + 'download/' + file, headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.headers['Content-Type'], 'application/octet-stream')
        self.assertNotEqual('', response.content)


if __name__ == "__main__":
    unittest.main()