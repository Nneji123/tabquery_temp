FROM python:3.8.13

WORKDIR /app

RUN apt-get -y update  && apt-get install -y \
  wget \
  ghostscript \
  python3-tk

RUN pip install --upgrade setuptools 

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

RUN python load_model.py

CMD uvicorn app:app --host 0.0.0.0 --port 8000