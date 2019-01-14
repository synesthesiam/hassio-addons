FROM synesthesiam/addon-base:latest
LABEL maintainer="Michael Hansen <hansen.mike@gmail.com>"

# Install system packages
RUN apt-get update && apt-get install -y python3 \
    python3-pip python3-dev build-essential \
    python3-setuptools \
    python3-scipy python3-numpy \
    libhdf5-dev \
    portaudio19-dev \
    alsa-utils \
    jq

RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir flask paho-mqtt

# Install tensorflow
RUN pip3 install --no-cache-dir tensorflow==1.8.0

# Install Mycroft Precise
RUN pip3 install --no-cache-dir pkgconfig cython
RUN pip3 install --no-cache-dir mycroft-precise==0.2.0

# Copy my stuff
COPY models /models
COPY *.py /
COPY *.html /
COPY run.sh /

ENTRYPOINT ["/run.sh"]