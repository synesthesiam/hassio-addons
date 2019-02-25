Snowboy Wake Listener
=========================

Small service that listens for a wake word with [snowboy](https://snowboy.kitt.ai).
Audio data is streamed in from [Rhasspy](https://github.com/synesthesiam/rhasspy) via [MQTT](http://mqtt.org/).


Building
----------

To build the Docker image, run `make docker` in the project root.

To create a local virtual environment, run the `create-venv.sh` shell script (expects a Debian distribution).


Running
---------

To run with Docker:

    docker run -it --network host synesthesiam/snowboy:1.3.0
    
To run in a virtual environement (after running `create-venv.sh`):

    ./run-venv.sh
    
This will connect to ports 5000 (PUB) and 5001 (PULL) on localhost. By default, the hotword is "snowboy".

Passing `--feedback` will let you see when audio data is being received and when the hotword is detected.
See `--help` for additional command-line arguments.
