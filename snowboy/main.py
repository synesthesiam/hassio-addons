#!/usr/bin/env python3
import os
import argparse
import subprocess
import logging
logging.basicConfig(level=logging.DEBUG)

from snowboy import snowboydetect, snowboydecoder
from nanomsg import Socket, SUB, SUB_SUBSCRIBE, PUSH

def main():
    # Find available universal models (.umdl)
    resource_dir = os.path.dirname(snowboydecoder.RESOURCE_FILE)
    umdl_dir = os.path.join(resource_dir, 'models')

    umdl_models = {
        os.path.splitext(name)[0]: os.path.join(umdl_dir, name)
        for name in os.listdir(umdl_dir)
    }

    # Parse arguments
    parser = argparse.ArgumentParser(description='snowboy')
    parser.add_argument('--pub-address',
                        help='nanomsg address of PUB socket (default=tcp://127.0.0.1:5000)',
                        type=str, default='tcp://127.0.0.1:5000')

    parser.add_argument('--pull-address',
                        help='nanomsg address of PULL socket (default=tcp://127.0.0.1:5001)',
                        type=str, default='tcp://127.0.0.1:5001')

    parser.add_argument('--payload', help='Payload string to send when wake word is detected (default=OK)',
                        type=str, default='OK')

    parser.add_argument('--model',
                        action='append',
                        type=str,
                        help='Path to snowboy model file or one of %s (default=snowboy)' % list(umdl_models.keys()),
                        default=[])

    parser.add_argument('--sensitivity',
                        action='append',
                        help='Model sensitivity (default=0.5)',
                        type=float,
                        default=[])

    parser.add_argument('--gain', help='Audio gain (default=1.0)',
                        type=float, default=1.0)

    parser.add_argument('--feedback', help='Show printed feedback', action='store_true')
    args = parser.parse_args()

    if len(args.model) == 0:
        args.model = ['snowboy']

    if len(args.sensitivity) == 0:
        args.sensitivity = [0.5]

    logging.debug(args)

    # Create detector(s)
    detectors = []

    for i, model in enumerate(args.model):
        model_path = umdl_models.get(model, model)
        detector = snowboydetect.SnowboyDetect(
            snowboydecoder.RESOURCE_FILE.encode(), model_path.encode())

        if len(args.sensitivity) > i:
            sensitivity_str = str(args.sensitivity[i]).encode()
            detector.SetSensitivity(sensitivity_str)

        detector.SetAudioGain(args.gain)
        detectors.append(detector)

    # Do detection
    try:
        payload = args.payload.encode()
        first_frame = False

        # Receive raw audio data via nanomsg
        with Socket(SUB) as sub_socket:
            sub_socket.connect(args.pub_address)
            sub_socket.set_string_option(SUB, SUB_SUBSCRIBE, '')
            logging.info('Connected to PUB socket at %s' % args.pub_address)

            with Socket(PUSH) as push_socket:
                # Response is sent via nanomsg
                push_socket.connect(args.pull_address)
                logging.info('Connected to PULL socket at %s' % args.pull_address)

                while True:
                    data = sub_socket.recv()  # audio data
                    if args.feedback:
                        print('.', end='', flush=True)

                    if not first_frame:
                        logging.debug('Receiving audio data from Rhasspy')
                        first_frame = True

                    for detector in detectors:
                        index = detector.RunDetection(data)
                        # Return is:
                        # -2 silence
                        # -1 error
                        #  0 voice
                        #  n index n-1
                        if index > 0:
                            # Hotword detected
                            if args.feedback:
                                print('!', end='', flush=True)

                            logging.info('Wake word detected!')

                            push_socket.send(payload)  # response
                            first_frame = False

    except KeyboardInterrupt:
        pass

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
