var centralController = new WebSocket("wss://" + location.host + ":8000");
centralController.onmessage = function (event) {
  console.log(event.data);
  msg = JSON.parse(event.data);
  console.log(msg);


  if (msg['event'] == "track_playback_started") {

    var trackName = msg['tl_track']['track']['name'];

    var artistsNames = "";
    for (var i = 0; i < msg['tl_track']['track']['artists'].length; i++) {
      if (i == 0) {
        artistName = msg['tl_track']['track']['artists'][i]['name'];
        artistsNames = artistsNames + artistName;
      }
      else {
        artistName = msg['tl_track']['track']['artists'][i]['name'];
        artistsNames = artistsNames + ", " + artistName;
      }
    }
    if (document.getElementById("trackName") || document.getElementById("artistName") || document.getElementById("albumName")) {
      document.getElementById("trackName").innerHTML = "";
      document.getElementById("artistName").innerHTML = "";
      document.getElementById("albumName").innerHTML = "";

      document.getElementById("trackName").appendChild(document.createTextNode(trackName));
      document.getElementById("artistName").appendChild(document.createTextNode(artistsNames));
      document.getElementById("albumName").appendChild(document.createTextNode(msg['tl_track']['track']['album']['name']));
    }

    var singleString = artistsNames + " - " + trackName;

    var metaElements = document.getElementsByClassName("now-playing-meta");
    for (var i = 0; i < metaElements.length; i++) {
      metaElements[i].innerHTML = "";
      metaElements[i].appendChild(document.createTextNode(singleString));
    }
  }

  else if (msg['id'] == "getTL" && document.getElementById("queue")) {
    trackList = msg;
    listDiv = document.getElementById("queue");
    listDiv.innerHTML = "";

    listElement = document.createElement('ol');
    listDiv.appendChild(listElement);
    if (trackList['result'].length > 1) {
      for (var i = 1; i < trackList['result'].length; i++) {
        trackListArtists = trackList['result'][i]['artists'];
        var artistsNames = "";
        for (var ii = 0; ii < trackListArtists.length; ii++) {
          if (ii == 0) {
            artistsNames = artistsNames + trackListArtists[ii]['name'];
          }
          else {
            artistsNames = artistsNames + ", " + trackListArtists[ii]['name'];
          }
        }
        text = document.createTextNode(artistsNames + " - " + trackList['result'][i]['name'])
        element = document.createElement('li');

        element.appendChild(text);
        listElement.appendChild(element);
      }
    }
    else {
      listDiv.innerHTML = "<p>No Tracks In Queue</p>"
    }
  }
}
