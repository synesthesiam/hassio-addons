FROM synesthesiam/opentts:ko-2.1
LABEL maintainer="Michael Hansen <hansen.mike@gmail.com>"

ENV LANG C.UTF-8

USER root
RUN if [ -f /data/options.json ]; then \
        cp /data/options.json /home/opentts/options.json; \
    fi

USER opentts

ENV CONFIG_PATH /home/opentts/options.json

COPY run.sh /home/opentts/run.sh

ENTRYPOINT ["/home/opentts/run.sh"]
