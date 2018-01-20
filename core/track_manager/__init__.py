import json
from toolkit import stat, verbo, debug
import globals
import webs
import track_manager.request
from random import shuffle

firstRun = True
isPlaying = False
playlist = []
currentPlTrack = 0
trackListLength = 0
leadingTrackByMe = None
trackList = []

def init_music_server():
    stat("Configuring music server")

    webs.client.send(track_manager.request.setConsume(True))
    verbo("Consume mode set")
    webs.client.send(track_manager.request.getPlayback())
    verbo("Getting playback state")
    webs.client.send(track_manager.request.getPlItems(globals.args.playlist))
    verbo("Getting playlist " + globals.args.playlist)
    stat("Finished Configuring")

def read_message(txtMessage):
    global firstRun
    global isPlaying
    global playlist
    global currentPlTrack
    global trackListLength
    global leadingTrackByMe
    global trackList

    message = json.loads(txtMessage)

    if ('event' in message):
        if (message['event'] == "playback_state_changed"):
            verbo("Playback State Changed from " + str(message['old_state']) + " to " + str(message['new_state']))

            if (message['old_state'] == "playing" and message['new_state'] == "stopped"): # this should ideally never run
                stat("Tracklist has no tracks! :O - Adding two")
                for i in range(2):
                    add_next_track() # add two tracks
                webs.client.send(track_manager.request.play())

            if (message['old_state'] == 'playing' and message['new_state'] == 'playing'): # if one track has finished and another is queued
                pass

            if (message['new_state'] == "playing"):
                isPlaying = True
            else:
                isPlaying = False

        elif (message['event'] == "track_playback_started"):
            webs.server.send(json.dumps(message).decode())

        elif (message['event'] == "track_playback_ended"):
            verbo("Track playback had ended.")

            ###

        elif (message['event'] == "tracklist_changed"):
            webs.client.send(track_manager.request.getTrackListLength()) # See how big the tracklist is
            webs.client.send(track_manager.request.getTrackList()) # Get the current tracklist for comparison
            verbo("Tracklist has changed. Will send to WebSocket server")

    if ('jsonrpc' in message):
        if (message['id'] == "checkPlay"):
            verbo("Got playback state")
            if (message['result'] == "playing"):
                isPlaying = True
                verbo("Currently playing")
            else:
                isPlaying = False
                verbo("Not currently playing")

        elif (message['id'] == "getPlItems"):
            stat("Reccieved the playlist")
            playlist = []
            for track in message['result']:
                debug("Adding track " + track['uri'])
                playlist.append(track['uri'])

            shuffle(playlist)
            verbo("Shuffled playlist")

            if (firstRun == True and isPlaying == False):
                for i in range(2):
                    add_next_track() # add two tracks
                webs.client.send(track_manager.request.play()) # Start playing
                stat("First track requested. Finished start up.")
                firstRun = False

        elif (message['id'] == "getTL"):
            trackList = []
            for track in message['result']:
                trackList.append(track)

        elif (message['id'] == "getTLLength"):
            prevLength = trackListLength
            trackListLength = message['result']

            if (prevLength < trackListLength): # if a track was added
                verbo("A track was added")
                if(trackListLength == 3 and leadingTrackByMe == True):
                    leadingTrackByMe = False
                    verbo("Leading track was added by me, will now delete")
                    webs.client.send(track_manager.request.removeTrack(trackList[1]['uri']))
                else:
                    verbo("No need to delete.")

            elif (prevLength > trackListLength): # if a track was removed
                verbo("A track was removed")

            if (trackListLength == 1): # if tracklist only has one track in it
                add_next_track()

def add_next_track():
    global currentPlTrack
    global leadingTrackByMe
    currentPlTrack += 1
    try:
        req = track_manager.request.addTrack(playlist[currentPlTrack])
    except:
        currentPlTrack = 0
        shuffle(playlist)
        req = track_manager.request.addTrack(playlist[currentPlTrack])
        verbo("Reached end of playlist. Repeating...")
    leadingTrackByMe = True
    webs.client.send(req)
