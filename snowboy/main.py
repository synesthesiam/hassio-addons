#!/usr/bin/env python3
import os
import io
import json
import wave
import time
import argparse
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

from snowboy import snowboydetect, snowboydecoder
import paho.mqtt.client as mqtt


def main():
    # Find available universal models (.umdl)
    resource_dir = os.path.dirname(snowboydecoder.RESOURCE_FILE)
    umdl_dir = os.path.join(resource_dir, "models")

    umdl_models = {
        os.path.splitext(name)[0]: os.path.join(umdl_dir, name)
        for name in os.listdir(umdl_dir)
    }

    # Parse arguments
    parser = argparse.ArgumentParser(description="snowboy")
    parser.add_argument(
        "--host", help="MQTT host (default=localhost)", type=str, default="localhost"
    )

    parser.add_argument(
        "--port", help="MQTT port (default=1883)", type=int, default=1883
    )

    parser.add_argument(
        "--username", help="MQTT username (default=)", type=str, default=""
    )

    parser.add_argument(
        "--password", help="MQTT password (default=)", type=str, default=""
    )

    parser.add_argument(
        "--reconnect",
        help="Seconds before MQTT reconnect (default=5, disabled=0)",
        type=float,
        default=5,
    )

    parser.add_argument(
        "--site-id", help="Hermes siteId (default=default)", type=str, default="default"
    )

    parser.add_argument(
        "--wakeword-id",
        help="Hermes wakewordId (default=default)",
        type=str,
        default="default",
    )

    parser.add_argument(
        "--model",
        action="append",
        type=str,
        help="Path to snowboy model file or one of %s (default=snowboy)"
        % list(umdl_models.keys()),
        default=[],
    )

    parser.add_argument(
        "--sensitivity",
        action="append",
        help="Model sensitivity (default=0.5)",
        type=float,
        default=[],
    )

    parser.add_argument(
        "--gain", help="Audio gain (default=1.0)", type=float, default=1.0
    )

    parser.add_argument("--feedback", help="Show printed feedback", action="store_true")
    args = parser.parse_args()

    if len(args.model) == 0:
        args.model = ["snowboy"]

    if len(args.sensitivity) == 0:
        args.sensitivity = [0.5]

    logging.debug(args)

    # Create detector(s)
    detectors = []

    for i, model in enumerate(args.model):
        model_path = umdl_models.get(model, model)
        detector = snowboydetect.SnowboyDetect(
            snowboydecoder.RESOURCE_FILE.encode(), model_path.encode()
        )

        if len(args.sensitivity) > i:
            sensitivity_str = str(args.sensitivity[i]).encode()
            detector.SetSensitivity(sensitivity_str)

        detector.SetAudioGain(args.gain)
        detectors.append(detector)

    # Set up MQTT
    topic_audio_frame = "hermes/audioServer/%s/audioFrame" % args.site_id
    topic_hotword_detected = "hermes/hotword/%s/detected" % args.wakeword_id

    client = mqtt.Client()

    # Login
    if len(args.username) > 0:
        logging.debug("Logging in as %s" % args.username)
        client.username_pw_set(args.username, args.password)

    # Set up MQTT
    def on_connect(client, userdata, flags, rc):
        client.subscribe(topic_audio_frame)
        client.subscribe("hermes/hotword/toggleOn")
        client.subscribe("hermes/hotword/toggleOff")
        logging.debug("Connected to %s:%s" % (args.host, args.port))

    first_frame = True
    listening = True

    def on_message(client, userdata, message):
        nonlocal first_frame, listening
        try:
            if message.topic == topic_audio_frame:
                if not listening:
                    return

                if first_frame:
                    logging.debug("Receiving audio data")
                    first_frame = False

                if args.feedback:
                    print(".", end="", flush=True)

                # Extract audio data
                with io.BytesIO(message.payload) as wav_buffer:
                    with wave.open(wav_buffer, mode="rb") as wav_file:
                        audio_data = wav_file.readframes(wav_file.getnframes())
                        for detector in detectors:
                            index = detector.RunDetection(audio_data)
                            # Return is:
                            # -2 silence
                            # -1 error
                            #  0 voice
                            #  n index n-1
                            if index > 0:
                                # Hotword detected
                                if args.feedback:
                                    print("!", end="", flush=True)

                                logging.debug("Hotword detected!")
                                payload = json.dumps(
                                    {
                                        "siteId": args.site_id,
                                        "modelId": args.model[0],
                                        "modelVersion": "",
                                        "modelType": "personal",
                                        "currentSensitivity": args.sensitivity[0],
                                    }
                                ).encode()

                                client.publish(topic_hotword_detected, payload)
                                first_frame = True
            elif message.topic == "hermes/hotword/toggleOn":
                listening = True
                logging.debug("On")
            elif message.topic == "hermes/hotword/toggleOff":
                listening = False
                logging.debug("Off")
        except Exception as e:
            logging.exception("on_message")

    client.on_connect = on_connect
    client.on_message = on_message

    def on_disconnect(client, userdata, rc):
        logging.warn("Disconnected")

        if args.reconnect > 0:
            time.sleep(args.reconnect)
            logging.debug("Reconnecting")
            client.connect(args.host, args.port)

    client.on_disconnect = on_disconnect

    connected = False
    while not connected:
        try:
            client.connect(args.host, args.port)
            connected = True
        except Exception as e:
            logging.exception("connect")

            if args.reconnect > 0:
                time.sleep(args.reconnect)
                logging.debug("Reconnecting")
            else:
                return

    try:
        logging.info("Listening")
        client.loop_forever()
    except KeyboardInterrupt:
        pass


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
