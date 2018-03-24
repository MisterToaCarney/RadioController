import websocket as websocketclient
from SimpleWebSocketServer import SimpleSSLWebSocketServer, WebSocket
import ssl
import thread
from threading import Lock
import time
import json
from random import shuffle

import atexit
import signal
import os
import subprocess
import sys

#Defining basic jsonrpc requests as a string because I am lazy

getPlayback = """{
  "method": "core.playback.get_state",
  "jsonrpc": "2.0",
  "params": {},
  "id": "checkPlay"
}"""


playReq = """{
  "method": "core.playback.play",
  "jsonrpc": "2.0",
  "params": {
    "tl_track": null,
    "tlid": null
  },
  "id": "play"
}"""

setConsume = """{
  "method": "core.tracklist.set_consume",
  "jsonrpc": "2.0",
  "params": {
    "value": true
  },
  "id": "setConsume"
}"""

getTrack = """{
  "method": "core.playback.get_current_track",
  "jsonrpc": "2.0",
  "params": {},
  "id": "getTrack"
}"""

getTrackList = """{
  "method": "core.tracklist.get_tracks",
  "jsonrpc": "2.0",
  "params": {},
  "id": "getTL"
}"""

# edit this for a different playlist
getPlItems = """{
  "method": "core.playlists.get_items",
  "jsonrpc": "2.0",
  "params": {
    "uri": "spotify:user:superconductor42:playlist:27Jbqg9tqkI9K8p8deNdu1"
  },
  "id": "getPlItems"
}"""

# secondary
"""getPlItems = {
  "method": "core.playlists.get_items",
  "jsonrpc": "2.0",
  "params": {
    "uri": "spotify:user:spotify:playlist:37i9dQZF1DX9G9wwzwWL2k"
  },
  "id": "getPlItems"
}"""



#empty_track = """{ "tl_track": {"track": {"album": { "name": "", "artists": ["name": ""]}, "name": "", "artists": [{"name": ""}]}}, "event": "track_playback_started"}"""
empty_track = """{ "tl_track": {"track": {"album": {"name": "", "artists": [{ "name": ""}]}, "name": "", "artists": [{ "name": ""}]}}, "event": "track_playback_started"}"""

playlist = []
currentPlTrack = 0
firstRun = True
queued_song = False


def on_message(ws, txtMessage):
  with print_lock:
    global isPlaying
    global playlist
    global currentPlTrack
    global firstRun
    global currentTrack
    global clients
    global nowPlaying
    global queued_song

    
    #print("- Message: " + txtMessage) # uncomment for verbose
    message = json.loads(txtMessage)


    if ('event' in message):
      if (message['event'] == "playback_state_changed"):
        print("-- I got: State change " + str(message['old_state']) + " -> " + str(message['new_state']))

        if (message['new_state'] == "playing" and message['old_state'] == "playing"):
          print("----> Playing a queued song. Marking for removal in 30 mins...")
          queued_song = True
          isPlaying = True

        elif(message['old_state'] == "paused" and message['new_state'] == "playing"): # if resumed
          isPlaying = True
          print("-- Resumed. Sending info to websocket...")
          for client in clients:
            client.sendMessage(json.dumps(nowPlaying).decode())

        elif (message['new_state'] == "playing"): # If is playing
          print("----> State is playing")
          isPlaying = True

        elif (message['old_state'] == "playing" and message['new_state'] == "paused"): # If account is being used elsewhere
          if (not os.path.exists('/var/www/radio/ws/manual.enable')):
            print("----> Requesting resume...") 
            ws.send(playReq)
          else:
            isPlaying = False
            print("----> Lock file exists, not requesting resume - sending empty track to websocket...")
            print(empty_track.encode('utf-8'))
            for client in clients:
               client.sendMessage(empty_track.decode()) 


        elif (message['old_state'] == "playing" and message['new_state'] == "stopped"): # If no more tracks in tracklist
          isPlaying = False
          print("----> State is stopped. Adding a random track from playlist...")
          queued_song = False;
          try:
            req = {
              "method": "core.tracklist.add", 
              "jsonrpc": "2.0", 
              "params": {"uri": playlist[currentPlTrack]}, 
              "id": "addTrack"
            }
          except:
            print("-- Reached end of playlist. Re-shuffling...")
            ws.send(getPlItems) # this is semi-pointless (even if there are new tracks, the server must be restarted)
            currentPlTrack = 0
            req = {
              "method": "core.tracklist.add", 
              "jsonrpc": "2.0", 
              "params": {"uri": playlist[currentPlTrack]}, 
              "id": "addTrack"
            }

          currentPlTrack += 1
          print("-- Requested: " + str(req))
          ws.send(json.dumps(req).encode('utf8'))
          ws.send(playReq)

        else:
          print("----> State is not playing. ")
          isPlaying = False
          
      elif (message['event'] == "track_playback_started"):

        print("-- I got: Track playback started. Sending to websocket server...")
        if queued_song == True:
          thread.start_new_thread(delete_track_from_recent, (message["tl_track"]["track"]["uri"],))
          print("----> Song was added by an external source, removing from recentTracks.txt in 30 mins...")
        else:
          print("----> Song was added by this script, not removing from recentTracks.txt")

        nowPlaying = message
        for client in clients:
          client.sendMessage(json.dumps(message).decode())
        


      
      elif (message['event'] == "tracklist_changed"): # This may not be needed later
        print("-- I got: Tracklist change. Sending tracklist to websocket server...")
        ws.send(getTrackList)
        

    elif ('jsonrpc' in message):
      if (message['id'] == "checkPlay"): #This should only run once
        print("-- I got: Initial play check")
        if (message['result'] == "playing"):
          isPlaying = True
          print("----> Currently playing")
        else:
          isPlaying = False
          print("----> Not playing")

      elif (message['id'] == "getTrack"):
        currentTrack = json.dumps(message)
        currentTrack = currentTrack.decode()

      elif (message['id'] == "getPlItems"): 
        print("-- Reccieved playlist")
        playlist = []
        for track in message['result']:
          playlist.append(track['uri'])
        shuffle(playlist)
	#print(playlist)

        if (firstRun == True and isPlaying == False):
          req = {
            "method": "core.tracklist.add", 
            "jsonrpc": "2.0", 
            "params": {"uri": playlist[currentPlTrack]}, 
            "id": "addTrack"
          }
          currentPlTrack += 1
          print("-- Requested: " + str(req))
          ws.send(json.dumps(req))
          ws.send(playReq)
          firstRun = False

      elif (message['id'] == "getTL"):
        for client in clients:
          client.sendMessage(json.dumps(message).decode())



def on_error(ws, error):
  if ("Errno 111" in str(error)):
    print("----> Server not running")
  else:
    print(error)

def on_close(ws):
    print("-- Server closed")

def on_open(ws):
  global connected
  connected = True
  def run(*args):
    ws.send(setConsume)
    ws.send(getPlayback)
    ws.send(getPlItems)
  thread.start_new_thread(run, ())

def start_mopidy():
  global music_server_proc
  try:
    if (sys.argv[1] == "-1"):
      print("----> Starting music server on card 1")
      music_server_proc = subprocess.Popen(["/usr/bin/mopidy", "--config", "/usr/share/mopidy/conf.d:/etc/mopidy/mopidy.conf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)    
    elif (sys.argv[1] == "-0"):
      print("----> Starting music server on card 0")
      music_server_proc = subprocess.Popen(["/usr/bin/mopidy", "--config", "/usr/share/mopidy/conf.d:/etc/mopidy/mopidy.conf:/etc/mopidy/xcard0.conf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
  except:
    print("----> Starting music server on card 1")
    music_server_proc = subprocess.Popen(["/usr/bin/mopidy", "--config", "/usr/share/mopidy/conf.d:/etc/mopidy/mopidy.conf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)  

def message_thread(ws, message):
  thread.start_new_thread(on_message, (ws, message))

def delete_track_from_recent(track_uri):
  track_uri = str(track_uri)
  time.sleep(1800)
  try:
    with open('/var/www/radio/scripts/recentTracks.txt', 'r') as fin:
      lines = fin.read().splitlines(True)
  except:
    pass
  with open('/var/www/radio/scripts/recentTracks.txt', 'w') as fout:
    for line in lines:
      if not track_uri in line:
        fout.write(line)


  #with open('/var/www/radio/scripts/recentTracks.txt', 'r') as fin: 
  #  data = fin.read().splitlines(True)
  #with open('/var/www/radio/scripts/recentTracks.txt', 'w') as fout:
  #  fout.writelines(data[1:])

def exit_handler():
  global music_server_proc
  print("- Stopping music server...")
  os.killpg(os.getpgid(music_server_proc.pid), signal.SIGTERM)


# Below is websocket server for telling webclients about songs.

clients = []

class SimpleServer(WebSocket):
  def handleMessage(self):
    pass
  def handleConnected(self):
    clients.append(self)
  def handleClose(self):
    clients.remove(self)


if __name__ == "__main__":
    global connected
    print_lock = Lock()
    atexit.register(exit_handler)

    cert = '/etc/letsencrypt/live/kamar.westbomb.net/fullchain.pem'
    key = '/etc/letsencrypt/live/kamar.westbomb.net/privkey.pem'

    try:
        print("- Deleting all recent tracks...")
        os.remove("/var/www/radio/scripts/recentTracks.txt")
    except:
        print("----> Unable to delete. File probably doesn't exist.")

    try:
      print("- Reading SSL/TLS certificates...")
      with open(cert) as f:
        pass
    except:
      print("!! FAILED TO READ SSL/TLS CERTIFICATE !!")
      print("Hard exiting...")
      os._exit(1);

    try:
      print("- Reading SSL/TLS key...")
      with open(key) as f:
        pass
    except:
      print("!! FAILED TO READ SSL/TLS PRIVATE KEY!!")
      print("Hard exiting...")
      os._exit(1);

    print("SSL/TLS check was successfull.")

    print("- Starting secure websocket server (WSS) on port 8000...")

    server = SimpleSSLWebSocketServer('', 8000, SimpleServer, cert, key)
    thread.start_new_thread(server.serveforever, ())
    
    print("- Starting music server...")
    thread.start_new_thread(start_mopidy, ())
    time.sleep(6)

    #websocketclient.enableTrace(True)
    ws = websocketclient.WebSocketApp("ws://localhost:6680/mopidy/ws",
                              on_message = message_thread,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    connected = False
    while (connected == False):
      print("-- Checking for running server...")
      ws.run_forever()
      time.sleep(2)
