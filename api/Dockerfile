FROM python:3.8.13-slim-bullseye

WORKDIR /app

RUN pip install --upgrade setuptools 

ADD . .

RUN pip install -r requirements.txt

EXPOSE 8000:8000

RUN python download.py

CMD python runserver.py