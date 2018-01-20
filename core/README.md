# RadioController Core
Core backend python scripts.

## Main Script: radiocontroller.py
Run with `python radiocontroller.py`

### Usage:
```
  -h, --help           show this help message and exit
  --soundcard {0,1}    Which sound card to use
  --playlist PLAYLIST  Spotify playlist to use (uri)
  --listen-port LPORT  Port for the websocket server to listen on.
  --mopidy-port MPORT  Port for connecting to the MPD WebSocket API
  --mopidy-host MHOST  The Mopidy (MPD) host. Usually localhost.
  --cert CERT          SSL/TLS Certificate file
  --key KEY            SSL/TLS key file
  -v, --verbose        Be verbose
  -d, --debug          Debug mode
```
