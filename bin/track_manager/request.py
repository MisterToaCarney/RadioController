# TrackManager Global functions
import json
from toolkit import stat, verbo

def getPlayback():
    verbo("Request to get playback state")
    req = {
      "method": "core.playback.get_state",
      "jsonrpc": "2.0",
      "params": {},
      "id": "checkPlay"
    }
    return(json.dumps(req))

def play():
    verbo("Request to play")
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
    verbo("Request to set consume to " + str(value))
    req = {
      "method": "core.tracklist.set_consume",
      "jsonrpc": "2.0",
      "params": {"value": value},
      "id": "setConsume"
    }
    return(json.dumps(req))

def getTrack():
    verbo("Request to get current track")
    req = {
      "method": "core.playback.get_current_track",
      "jsonrpc": "2.0",
      "params": {},
      "id": "getTrack"
    }
    return(json.dumps(req))

def getTrackList():
    verbo("Request to get track list")
    req = {
      "method": "core.tracklist.get_tracks",
      "jsonrpc": "2.0",
      "params": {},
      "id": "getTL"
    }
    return(json.dumps(req))

def getPlItems(playlist):
    verbo("Request to get " + str(playlist) + " playlist items")
    req = {
      "method": "core.playlists.get_items",
      "jsonrpc": "2.0",
      "params": {"uri": playlist},
      "id": "getPlItems"
    }
    return(json.dumps(req))

def addTrack(track):
    verbo("Request to add track " + str(track) + " to tracklist")
    req = {
      "method": "core.tracklist.add",
      "jsonrpc": "2.0",
      "params": {"uri": track},
      "id": "addTrack"
    }
    return(json.dumps(req))

def removeTrack(track):
    verbo("Request to remove track " + str(track) + " from tracklist")
    req = {
      "method": "core.tracklist.remove",
      "jsonrpc": "2.0",
      "params": {"criteria": {'uri': [track]}},
      "id": "removeTrack"
    }
    return(json.dumps(req))

def getTrackListLength():
    verbo("Request to get tracklist length")
    req = {
        "method": "core.tracklist.get_length",
        "jsonrpc": "2.0",
        "params": {},
        "id": "getTLLength"
    }
    return(json.dumps(req))
