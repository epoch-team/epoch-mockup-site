FROM ubuntu:18.04

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y locales curl python3-distutils git vim \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && mkdir /code \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

WORKDIR /

RUN git clone https://github.com/epoch-team/epoch-mockup-site.git workspace \
    && chmod -R 777 /workspace

WORKDIR /workspace

RUN     echo "django"   >   requirements.txt \
    &&  echo "requests" >>  requirements.txt \
    &&  pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "cd /workspace/src; python3 manage.py runserver 0.0.0.0:8000; while :; do sleep 60; done"]

