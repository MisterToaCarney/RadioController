#!/bin/bash

resp=$(curl -X POST -H Content-Type:application/json -d '{
  "method": "core.tracklist.add",
  "jsonrpc": "2.0",
  "params": {
    "uri": "'"$1"'"
  },
  "id": 1
}' http://localhost:6680/mopidy/rpc)

if [ "$resp" == '{"jsonrpc": "2.0", "id": 1, "result": []}' ]; then
echo "URI Not Found"
exit
fi
echo "$resp"
echo $1 >> /var/www/radio/scripts/recentTracks.txt
