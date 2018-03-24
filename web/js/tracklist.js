var oReq = new XMLHttpRequest();
oReq.addEventListener("load", requestListener);
oReq.open("GET", "/action/list.php");
oReq.send()
var trackList;
function requestListener() {
  trackList = JSON.parse(this.responseText);
  listDiv = document.getElementById("queue");
  listDiv.innerHTML = "";

  listElement = document.createElement('ol');
  listDiv.appendChild(listElement);
  if (trackList['result'].length > 1) {
    for (var i = 1; i < trackList['result'].length; i++) {
      var artistsNames = "";
      var trackListArtists = trackList['result'][i]['artists'];
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
