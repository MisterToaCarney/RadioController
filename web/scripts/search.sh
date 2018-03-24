#!/bin/sh

curl -X POST -H Content-Type:application/json -d '{
  "method": "core.library.search",
  "jsonrpc": "2.0",
  "params": {
    "any": ["'"$1"'"]
  },
  "id": 1
}' http://localhost:6680/mopidy/rpc
