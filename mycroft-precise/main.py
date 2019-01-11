#!/usr/bin/env python3
import os
import argparse
import subprocess
import threading
import logging
logging.basicConfig(level=logging.DEBUG)

from precise_runner import PreciseEngine, PreciseRunner
from nanomsg import Socket, SUB, SUB_SUBSCRIBE, PUSH

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='mycroft-precise')
    parser.add_argument('--pub-address',
                        help='nanomsg address of PUB socket (default=tcp://127.0.0.1:5000)',
                        type=str, default='tcp://127.0.0.1:5000')

    parser.add_argument('--pull-address',
                        help='nanomsg address of PULL socket (default=tcp://127.0.0.1:5001)',
                        type=str, default='tcp://127.0.0.1:5001')

    parser.add_argument('--payload', help='Payload string to send when wake word is detected (default=OK)',
                        type=str, default='OK')

    parser.add_argument('--model',
                        type=str,
                        required=True,
                        help='Path to model file (.pb)')

    parser.add_argument('--sensitivity',
                        help='Model sensitivity (default=0.5)',
                        type=float,
                        default=0.5)

    parser.add_argument('--trigger-level', help='Number of trigger events required (default=3)',
                        type=int, default=3)

    parser.add_argument('--feedback', help='Show printed feedback', action='store_true')
    args = parser.parse_args()

    # Create runner
    engine = PreciseEngine('precise-engine', args.model)
    stream = ByteStream()

    with Socket(PUSH) as push_socket:
        # Response is sent via nanomsg
        push_socket.connect(args.pull_address)
        logging.info('Connected to PULL socket at %s' % args.pull_address)

        first_frame = False

        def on_activation():
            nonlocal first_frame

            # Hotword detected
            if args.feedback:
                print('!', end='', flush=True)

            push_socket.send(payload)  # response
            logging.info('Wake word detected!')
            first_frame = False

        runner = PreciseRunner(engine, stream=stream,
                               sensitivity=args.sensitivity,
                               trigger_level=args.trigger_level,
                               on_activation=on_activation)

        runner.start()

        # Do detection
        try:
            payload = args.payload.encode()

            # Receive raw audio data via nanomsg
            with Socket(SUB) as sub_socket:
                sub_socket.connect(args.pub_address)
                sub_socket.set_string_option(SUB, SUB_SUBSCRIBE, '')
                logging.info('Connected to PUB socket at %s' % args.pub_address)

                while True:
                    data = sub_socket.recv()  # audio data
                    if args.feedback:
                        print('.', end='', flush=True)

                    if not first_frame:
                        logging.debug('Receiving audio data from Rhasspy')
                        first_frame = True

                    # Write to in-memory stream
                    stream.write(data)

        except KeyboardInterrupt:
            pass

        try:
            stream.close()
            runner.stop()
        except:
            pass

# -----------------------------------------------------------------------------

class ByteStream:
    def __init__(self):
        self.buffer = bytes()
        self.event = threading.Event()
        self.closed = False

    def read(self, n=-1):
        # Block until enough data is available
        while len(self.buffer) < n:
            if not self.closed:
                self.event.wait()
            else:
                self.buffer += bytearray(n - len(self.buffer))

        chunk = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return chunk

    def write(self, data):
        if self.closed:
            return

        self.buffer += data
        self.event.set()

    def close(self):
        self.closed = True
        self.event.set()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
