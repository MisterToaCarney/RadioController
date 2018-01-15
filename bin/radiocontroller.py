#!/usr/bin/env python

import argparse
import atexit
import signal
from time import sleep

from toolkit import stat

from webs import *
import mopidy

parser = argparse.ArgumentParser(description="Flex FM Radio Automation Backend")
parser.add_argument('--soundcard',  type=int, dest="card", help="Which sound card to use", choices=[0, 1], default=1);
parser.add_argument('--playlist', type=str, help="Spotify playlist to use (uri)", default="spotify:user:superconductor42:playlist:27Jbqg9tqkI9K8p8deNdu1")
parser.add_argument("--listen-port", dest="lport", type=int, help="Port for the websocket server to listen on.", default=8000)
parser.add_argument("--mopidy-port", dest="mport", type=int, help="Port for connecting to the MPD WebSocket API", default=6680)
parser.add_argument("--mopidy-host", dest="mhost", type=str, help="The Mopidy (MPD) host. Usually localhost.", default="localhost")
parser.add_argument('--cert', type=str, help="SSL/TLS Certificate file", default="/etc/letsencrypt/live/kamar.westbomb.net/fullchain.pem")
parser.add_argument("--key", type=str, help="SSL/TLS key file", default="/etc/letsencrypt/live/kamar.westbomb.net/privkey.pem")
args = parser.parse_args()


def exit_handler():
    stat("Will now exit")
    mopidy.stop_music_server()

atexit.register(exit_handler)

stat("Calling for start of mopidy")
mopidy.start_music_server(args)
stat("Call completed")
stat("Calling for start of WebSocket server")
server.start_websocket_server(args.cert, args.key, args.lport)
stat("Call completed")
stat("Calling for start of websocket client")
stat("Root will now hand off control to websocket client.")
client.start_websocket_client(args.mhost, args.mport)
stat("Call completed")
