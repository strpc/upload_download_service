#upload_download_service
---
Тестовое задание:
```
1)  Написать сервис, с функционалом:
    a.  upload -> загрузить  файл, сохранить файл в файловой системе,
        сформировать уникальную ссылку для скачивания файла
    b.  check -> проверить наличие ранее загруженного файла по ссылке
    c.  download -> скачать ранее загруженный файл используя ссылку
2)  реализовать ограничение скорости upload и download
3)  реализовать этот сервис в формате multithreading или async
4)  написать тесты
5)  завернуть в docker (ubuntu | alpine)

Плюсом будет:
-   соответствие pep8
-   документирование кода
-   аннотация типов
-   наличие логов
-   нагрузочный тест
-   обработка возможных ошибок

Ограничение:
В реализации основного кода сервиса использовать только стандартные библиотеки Python 3.6(3.7)
```
------------
API:
**Отправка файла**
```
> POST /upload/ HTTP/1.1
> Host: 127.0.0.1:8000
> Content-Disposition: attachment
> Content-Type: application/pdf
> Content-Length: 345646
```
Response:
```
< HTTP/1.0 201 Created
< Content-Type: application/json
{
  'status': 201,
  'fileisuploaded': 'test.pdf',
  'linkforcheck': '0.0.0.0:8000/check/test.pdf',
  'linkfordownload': '0.0.0.0:8000/download/test.pdf'
}
```
<br>

**Проверка файла**
```
> GET /check/test.pdf HTTP/1.1
> Host: 127.0.0.1:8000
```
Response:
```
< HTTP/1.0 200 OK
< Content-Type: application/json
{
  'status': 200,
  'file': 'test.pdf',
  'message': 'is ready to download'
}
```
<br>

**Загрузка файла**
```
> GET /download/test.pdf HTTP/1.1
> Host: 127.0.0.1:8000
```
Response:
```
< HTTP/1.0 200 OK
< Content-Type: application/octet-stream

*bytes of file*
```
-----

**Результаты нагрузочного тестирования:**
8 потоков, 200 соединений, продолжительность 30 секунд, таймаут на запросы 2 секунды
```
wrk -t8 -c200 -d30s --timeout 2s http://localhost:8000/check/test.pdf

Running 30s test @ http://localhost:8000/check/test.pdf
  8 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    60.28ms   24.08ms 251.99ms   75.90%
    Req/Sec    34.63     22.98   160.00     67.41%
  3863 requests in 30.08s, 456.47KB read
  Socket errors: connect 0, read 5404, write 39, timeout 0
Requests/sec:    128.43
Transfer/sec:     15.18KB
```
----
**Запуск:**
```
git clone https://github.com/strpc/upload_download_service.git
docker build -t=upload_download_service .
docker run -d --rm --name upload_download_service -p 8000:8000 upload_download_service
or
cd upload_download_service
python3 server.py
```
<br>

Для написания тестов использовалась библиотека `requests`(`pip install requests` или `pip install -r requirements.txt`)