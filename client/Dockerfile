FROM python:3.5-alpine


EXPOSE 5002

WORKDIR /capp

RUN pip install --upgrade pip

ADD requirements.txt /capp

RUN apk add --no-cache --update gcc libc-dev linux-headers
RUN pip install -r requirements.txt

COPY . /capp
ENTRYPOINT ["python", "client.py"]