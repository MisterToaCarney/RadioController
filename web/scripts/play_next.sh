#!/bin/sh

curl -X POST -H Content-Type:application/json -d '{
  "method": "core.tracklist.add",
  "jsonrpc": "2.0",
  "params": {
    "at_position": 1,
    "uri": "'"$1"'"
  },
  "id": 1
}' http://localhost:6680/mopidy/rpc
