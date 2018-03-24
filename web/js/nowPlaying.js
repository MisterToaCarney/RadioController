var track;
var oReq = new XMLHttpRequest();
oReq.addEventListener("load", requestListener);
oReq.open("GET", "/action/get_track.php");
oReq.send();

function requestListener() {
  track = JSON.parse(this.responseText);
  console.log(track);

  var trackName = track['result']['name'];

  var artistsNames = "";
  for (var i = 0; i < track['result']['artists'].length; i++) {
    if (i == 0) {
      var artistName = track['result']['artists'][i]['name'];
      artistsNames = artistsNames + artistName;
    }
    else {
      var artistName = track['result']['artists'][i]['name'];
      artistsNames = artistsNames + ", " + artistName;
    }
  }

  var albumName = track['result']['album']['name'];

  if (document.getElementById("trackName") || document.getElementById("artistName") || document.getElementById("albumName")) {
    document.getElementById("trackName").innerHTML = "";
    document.getElementById("artistName").innerHTML = "";
    document.getElementById("albumName").innerHTML = "";

    document.getElementById("trackName").appendChild(document.createTextNode(trackName));
    document.getElementById("artistName").appendChild(document.createTextNode(artistsNames));
    document.getElementById("albumName").appendChild(document.createTextNode(albumName));
  }

  var singleString = artistsNames + " - " + trackName;

  var metaElements = document.getElementsByClassName("now-playing-meta");
  for (var i = 0; i < metaElements.length; i++) {
    metaElements[i].innerHTML = "";
    metaElements[i].appendChild(document.createTextNode(singleString));
  }

}
