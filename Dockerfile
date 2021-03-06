FROM ubuntu:16.04

MAINTAINER Janis Lesinskis

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


RUN apt-get update -y && apt-get -y install \
	python3-pip \
	ffmpeg \
	sox \
	git

# -- Install Application into container:
RUN mkdir /app
WORKDIR /app

RUN pip3 install pipenv

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
# -- Install dependencies:
RUN pipenv install --deploy --system

COPY . /app

EXPOSE 8080

ENTRYPOINT [ "python3" ]

CMD [ "transcription_API_server.py" ]
