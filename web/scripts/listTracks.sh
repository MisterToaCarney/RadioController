#!/bin/sh

curl -X POST -H Content-Type:application/json -d '{
  "method": "core.tracklist.get_tracks",
  "jsonrpc": "2.0",
  "params": {},
  "id": 1
}' http://localhost:6680/mopidy/rpc
