FROM python:3.7.7-alpine3.11
MAINTAINER https://github.com/strpc
COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "./upload_download_service/server.py"]