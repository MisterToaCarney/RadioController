import json
from toolkit import stat
import globals
import webs.client
import track_manager.request
from random import shuffle

firstRun = True
isPlaying = False
playlist = []
currentPlTrack = 0

def init_music_server():
    stat("Configuring music server")

    webs.client.send(track_manager.request.setConsume(True))
    stat("Consume mode set")
    webs.client.send(track_manager.request.getPlayback())
    stat("Getting playback state")
    webs.client.send(track_manager.request.getPlItems(globals.args.playlist))
    stat("Getting playlist " + globals.args.playlist)

def read_message(txtMessage):
    global firstRun
    global isPlaying
    global playlist
    global currentPlTrack

    message = json.loads(txtMessage)

    if ('event' in message):
        if (message['event'] == "playback_state_changed"):
            stat("Playback State Changed from " + str(message['old_state']) + " to -> " + str(message['new_state']))

            ###

        elif (message['event'] == "track_playback_started"):
            stat("Track playback has started. Will send to WebSocket server")

            ###

        elif (message['event'] == "tracklist_changed"):
            stat("Tracklist has changed. Will send to WebSocket server")


    if ('jsonrpc' in message):
        if (message['id'] == "checkPlay"):
            stat("Got playback state")
            if (message['result'] == "playing"):
                isPlaying = True
                stat("Currently playing")
            else:
                isPlaying = False
                stat("Not currently playing")

        elif (message['id'] == "getPlItems"):
            stat("Reccieved the playlist")
            playlist = []
            for track in message['result']:
                if (globals.args.verbose):
                    stat("Adding track " + track['uri'])
                playlist.append(track['uri'])

            shuffle(playlist)
            stat("Shuffled playlist")

            if (firstRun == True and isPlaying == False):
                webs.client.send(track_manager.request.addTrack(playlist[currentPlTrack])) # add current track to tracklist
                webs.client.send(track_manager.request.play()) # Play the track
                currentPlTrack += 1
                stat("First track requested. Finished start up.")
                firstRun = False
