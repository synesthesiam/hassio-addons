FROM python:3.6
LABEL maintainer="Michael Hansen <hansen.mike@gmail.com>"

RUN apt-get update && apt-get install -y python3-pip python3-dev \
    jq \
    libasound2-dev swig \
    portaudio19-dev \
    libatlas-base-dev \
    libnanomsg-dev

COPY snowboy-1.3.0.tar.gz /
COPY nanomsg-python-master.zip /

RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir flask
RUN pip3 install --no-cache-dir /snowboy-1.3.0.tar.gz
RUN pip3 install --no-cache-dir /nanomsg-python-master.zip

COPY models/ /models
COPY *.py /
COPY *.html /
COPY run.sh /
ENTRYPOINT ["/run.sh"]