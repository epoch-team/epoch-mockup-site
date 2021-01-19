FROM ubuntu:18.04

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y locales curl python3-distutils git vim \
#   && apt-get install -y apache2 \
    && touch /etc/apt/sources.list.d/nginx.list \
    && echo "deb http://nginx.org/packages/ubuntu/ precise nginx" >> /etc/apt/sources.list.d/nginx.list \
    && echo "deb-src http://nginx.org/packages/ubuntu/ precise nginx" >> /etc/apt/sources.list.d/nginx.list \
    && curl http://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-get update \
    && apt-get install -y nginx \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && mkdir /code \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

WORKDIR /workspace

RUN     echo "django"   >   requirements.txt \
    &&  echo "requests" >>  requirements.txt \
    &&  pip install -r requirements.txt

# for Apache2
#RUN	chmod -R 777 /var/www \
#    &&  chmod -R 777 /var/run \
#    &&  chmod -R 777 /var/lock


COPY . /workspace

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "while :; do sleep 60; done"]

