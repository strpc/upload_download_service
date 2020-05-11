import os
from functools import wraps
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from uuid import uuid4
import threading

from config import IP, PORT, STORAGE
import logger


def mult_threading(func):
    @wraps(func)
    def wrapper(*args_, **kwargs_):
        func_thread = threading.Thread(target=func,
                                       args=tuple(args_),
                                       kwargs=kwargs_)
        func_thread.start()
        return func_thread
    return wrapper


class Handler(BaseHTTPRequestHandler):

    def _response(self, msg):
        """
        Сериализатор

        :param msg: - сообщение, которое нужно сериализировать.
        """
        return str(msg).encode("utf8")

    @staticmethod
    def _check_file(filename):
        """
        Проверка существует ли файл в файловой системе.

        :param filename: - имя файла.
        """
        for f in os.listdir(os.path.join(os.getcwd(), STORAGE)):
            if f == filename:
                return True
        return False

    def _file_not_found(self, filename):
        """
        Отправка ответа "файл не найден".

        :param filename: - имя файла.
        """
        self.send_response_only(400)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(self._response({
            "status": 400,
            "file": filename,
            "message": "is not found"
        }))

    def do_GET(self):
        """GET-запросы"""
        route = self.path.split('/')
        route = list(filter(None, route))
        exist = None

        # проверка, что переход по url /check/example.jpg
        if route and route[0] == 'check' and route[-1] != 'check':
            filename = route[-1]
            exist = self._check_file(filename)
            # проверка, сущестует ли файл.
            if exist == True:
                self.send_response_only(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(self._response({
                    "status": 200,
                    "file": filename,
                    "message": "is ready to download"
                }))
                logger.do_write_info(
                    f'Была осуществлена проверка наличия файла {filename}',
                    'headers:',
                    *self.headers
                )
            # если не существует, ответ "Not found", статус 400
            else:
                self._file_not_found(filename)
                logger.do_write_error(
                    'Попытка обращения к несуществующему файлу.',
                    self.path,
                    'headers:',
                    *self.headers
                )

        # проверка, что переход по url /download/example.jpg
        elif route and route[0] == 'download' and route[-1] != 'download':
            filename = route[-1]
            exist = self._check_file(filename)
            # проверка, сущестует ли файл.
            if exist:
                with open(os.path.join(os.getcwd(), STORAGE, filename),
                          'rb') as f:
                    self.send_response_only(200)
                    self.send_header("Content-Type",
                                     "application/octet-stream")
                    self.end_headers()
                    self.wfile.write(f.read())
                logger.do_write_info(
                    f'Файл {filename} был загружен пользователем',
                    'headers:',
                    *self.headers
                )
            # если не существует, ответ "Not found",
            else:
                self._file_not_found(filename)
                logger.do_write_error(
                    'Отсутствует файл для отправки. {filename}.',
                    'headers:',
                    *self.headers
                )
        # если переход по стороннему url, то ответ 'page not found'
        else:
            self.send_response_only(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(self._response({
                'status': 404,
                'message': 'page not found'
            }))
            logger.do_write_error(
                f'Переход на некорректный адрес. {self.path} headers:',
                *self.headers
            )

    def do_POST(self):
        """POST-запросы"""
        # проверка, что в заголовке есть информация о загружаемом файле
        if self.headers.get('Content-type', None) is None:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(self._response({
                'status': 403,
                'message': 'headers not found'
            }))
            logger.do_write_error(
                'Попытка обращения к несуществующему адресу. headers:',
                *self.headers
            )
            return

        route = self.path.split('/')
        route = list(filter(None, route))
        expansion = self.headers.get('Content-type', None)
        expansion = expansion.split('/')[-1] if expansion != None else None

        # проверка, что переход по url /upload/
        if route and route[0] == 'upload' and route[-1] == 'upload':
            content_length = self.headers.get('Content-Length', None)
            # проверка, что файл прикреплен
            if content_length is not None and content_length != '0':
                data = self.rfile.read(int(content_length))
                filename = self.headers.get('Filename',
                                            f"{uuid4().hex}.{expansion if expansion else ''}")

                try:
                    with open(os.path.join(os.getcwd(), STORAGE, filename),
                              'wb') as f:
                        f.write(data)
                    self.send_response_only(201)
                    self.send_header(
                        'Content-Type', 'application/json'
                    )
                    self.end_headers()
                    self.wfile.write(self._response(
                        {
                            'status': 201,
                            'file is uploaded': filename,
                            'link for check': f"{IP}:{PORT}/check/{filename}",
                            'link for download': f"{IP}:{PORT}/download/{filename}",
                        }))
                    logger.do_write_info(
                        f'Файл {filename} был загружен в директорию /{STORAGE}/'
                    )
                except Exception as error:
                    self.send_response_only(403)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(self._response(
                        {
                            'status': 403,
                            'error': 'file is not uploaded',
                        }))
                    logger.do_write_error(
                        'Произошла ошибка при получении файла.',
                        error,
                        self.path,
                        'headers:',
                        *self.headers
                    )
            # если файл не прикреплен, то ответ 409
            else:
                self.send_response(409)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(self._response(
                    {
                        'status': 409,
                        'error': 'file not attached',
                    }))
                logger.do_write_error(
                    f'Отсутствует файл для загрузки. {self.path}. headers:',
                    *self.headers
                )
        # если переход по стороннему url, то ответ 'page not found'
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(self._response({
                'status': 404,
                'message': 'page not found'
            }))
            logger.do_write_error(
                f'Попытка обращения к несуществующему адресу. {self.path}.'
                'headers:',
                *self.headers
            )


@mult_threading
def run(ip='127.0.0.1', port=8000):
    server_address = (ip, port)
    httpd = ThreadingHTTPServer(server_address, Handler)
    print(f'Server is running. {ip}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    if not os.path.exists(os.path.join(os.getcwd(), STORAGE)):
        try:
            os.mkdir(os.path.join(os.getcwd(), STORAGE))
        except Exception as e:
            logger.logging.error(
                'Ошибка при создании папки для хранилища файлов. '
                'Возможно проблема с правами доступа.')
    run(ip=IP, port=PORT)
