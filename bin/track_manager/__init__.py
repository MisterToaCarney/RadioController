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
trackListLength = 0
addedByMe = None
leadingTrackByMe = None
trackList = []

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
    global trackListLength
    global addedByMe
    global leadingTrackByMe
    global trackList

    message = json.loads(txtMessage)

    if ('event' in message):
        if (message['event'] == "playback_state_changed"):
            stat("Playback State Changed from " + str(message['old_state']) + " to " + str(message['new_state']))

            if (message['old_state'] == "playing" and message['new_state'] == "stopped"): # this should ideally never run
                stat("Tracklist has no tracks! :O - Adding two")
                addedByMe = True
                leadingTrackByMe = True
                for i in range(2):
                    currentPlTrack += 1
                    try:
                        req = track_manager.request.addTrack(playlist[currentPlTrack])
                    except:
                        currentPlTrack = 0
                        shuffle(playlist)
                        req = track_manager.request.addTrack(playlist[currentPlTrack])
                        stat("Reached end of playlist. Repeating...")
                    webs.client.send(req)
                webs.client.send(track_manager.request.play())

            if (message['old_state'] == 'playing' and message['new_state'] == 'playing'): # if one track has finished and another is queued
                pass

            if (message['new_state'] == "playing"):
                isPlaying = True
            else:
                isPlaying = False

        elif (message['event'] == "track_playback_started"):
            stat("Track playback has started. Will send to WebSocket server")

        elif (message['event'] == "track_playback_ended"):
            stat("Track playback had ended.")

            ###

        elif (message['event'] == "tracklist_changed"):
            webs.client.send(track_manager.request.getTrackListLength()) # See how big the tracklist is
            webs.client.send(track_manager.request.getTrackList()) # Get the current tracklist for comparison
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
                addedByMe = True
                leadingTrackByMe = True
                webs.client.send(track_manager.request.addTrack(playlist[currentPlTrack])) # add current track to tracklist
                currentPlTrack += 1
                webs.client.send(track_manager.request.addTrack(playlist[currentPlTrack])) # line up next track
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
                stat("!! A track was added")
                if (addedByMe == True):
                    stat("!! Track was added by me. Will not delete.")
                    addedByMe = False
                elif (addedByMe == False):
                    stat("!! Track was added externally please standby...")
                    if(trackListLength == 3 and leadingTrackByMe == True):
                        leadingTrackByMe = False
                        stat("!!!! Leading track was added by me, will now delete")
                        webs.client.send(track_manager.request.removeTrack(trackList[1]['uri']))
                    elif(trackListLength > 3):
                        stat("!!!! Leading track was not added by me, will not delete")

            elif (prevLength > trackListLength): # if a track was removed
                stat("!! A track was removed")

            if (trackListLength == 1): # if tracklist only has one track in it
                currentPlTrack += 1
                try:
                    req = track_manager.request.addTrack(playlist[currentPlTrack]) # add track
                except: # if at end of playlist :
                    currentPlTrack = 0 # go to beginning
                    shuffle(playlist) # reshuffle
                    req = track_manager.request.addTrack(playlist[currentPlTrack]) # add track
                    stat("Reached end of playlist. Repeating...")
                addedByMe = True
                leadingTrackByMe = True
                webs.client.send(req)
