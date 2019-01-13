FROM python:3.6
LABEL maintainer="Michael Hansen <hansen.mike@gmail.com>"

RUN apt-get update && apt-get install -y python3 \
    python3-pip python3-dev \
    python3-setuptools \
    build-essential swig \
    jq \
    libasound2-dev \
    portaudio19-dev \
    libatlas-base-dev

COPY snowboy-1.3.0.tar.gz /

RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir flask paho-mqtt
RUN pip3 install --no-cache-dir /snowboy-1.3.0.tar.gz

COPY models/ /models
COPY *.py /
COPY *.html /
COPY run.sh /
ENTRYPOINT ["/run.sh"]