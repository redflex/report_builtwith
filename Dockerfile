FROM alpine:3.4 as tester

RUN apk add -U \
  python \
  py-pip

COPY app/ /app/

RUN /usr/bin/python2.7 \
    -mpip install \
        pytest \
        pytest-cover

RUN /usr/bin/python2.7 \
    -mpy.test \
        --cov-report term-missing \
        --cov=bwlib /app/test/

#######################

FROM alpine:3.4
MAINTAINER @ashmastaflash

RUN apk add -U \
  python

COPY app/ /app/

RUN adduser \
        -D \
        -s /bin/sh \
        -h /app \
        builtwithreporter

RUN chown -R builtwithreporter:builtwithreporter /app

ENTRYPOINT /usr/bin/python2.7 /app/application.py
