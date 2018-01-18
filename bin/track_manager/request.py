# TrackManager Global functions
import json

def getPlayback():
    req = {
      "method": "core.playback.get_state",
      "jsonrpc": "2.0",
      "params": {},
      "id": "checkPlay"
    }
    return(json.dumps(req))

def play():
    req = {
      "method": "core.playback.play",
      "jsonrpc": "2.0",
      "params": {
        "tl_track": None,
        "tlid": None
      },
      "id": "play"
    }
    return(json.dumps(req))

def setConsume(value):
    req = {
      "method": "core.tracklist.set_consume",
      "jsonrpc": "2.0",
      "params": {"value": value},
      "id": "setConsume"
    }
    return(json.dumps(req))

def getTrack():
    req = {
      "method": "core.playback.get_current_track",
      "jsonrpc": "2.0",
      "params": {},
      "id": "getTrack"
    }
    return(json.dumps(req))

def getTrackList():
    req = {
      "method": "core.tracklist.get_tracks",
      "jsonrpc": "2.0",
      "params": {},
      "id": "getTL"
    }
    return(json.dumps(req))

def getPlItems(playlist):
    req = {
      "method": "core.playlists.get_items",
      "jsonrpc": "2.0",
      "params": {"uri": playlist},
      "id": "getPlItems"
    }
    return(json.dumps(req))

def addTrack(track):
    req = {
      "method": "core.tracklist.add",
      "jsonrpc": "2.0",
      "params": {"uri": track},
      "id": "addTrack"
    }
    return(json.dumps(req))

def removeTrack(track):
    req = {
      "method": "core.tracklist.remove",
      "jsonrpc": "2.0",
      "params": {"criteria": {'uri': [track]}},
      "id": "removeTrack"
    }
    return(json.dumps(req))

def getTrackListLength():
    req = {
        "method": "core.tracklist.get_length",
        "jsonrpc": "2.0",
        "params": {},
        "id": "getTLLength"
    }
    return(json.dumps(req))
