#!/bin/sh

curl -X POST -H Content-Type:application/json -d '{
  "method": "core.playback.get_current_track",
  "jsonrpc": "2.0",
  "params": {},
  "id": 1
}' http://localhost:6680/mopidy/rpc
