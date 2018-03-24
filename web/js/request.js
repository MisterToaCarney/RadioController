function reqListener () {
  var currentSongArrayPos;
  var currentSearch;
  var noResult = true;

  obj = JSON.parse(this.responseText);
  console.log(obj);
  var resultBox = document.getElementById("results");
  resultBox.innerHTML = null;

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", "/scripts/recentTracks.txt?rand=" + Math.random(), false ); // false for synchronous request
  xmlHttp.send( null );

  var recentTracks = xmlHttp.responseText;

  mainTable = document.createElement("table")
  for (currentSearch = 0; currentSearch < obj['result'].length; currentSearch++) {

    if (typeof obj['result'][currentSearch]['tracks'] != 'undefined') {
      noResult = false;
      for (currentSongArrayPos = 0; currentSongArrayPos < obj['result'][currentSearch]['tracks'].length; currentSongArrayPos++) {
        resultRow = document.createElement("tr"); //create our table row
        resultRow.classList.add("result"); //add class 'result' to our table row

        playButtonTd = document.createElement('td') //create td for playbutton
        playButton = document.createElement('button'); //create button
        playButtonTd.appendChild(playButton); //add playbutton to td
        resultRow.appendChild(playButtonTd); //add td to tr

        trackElement = document.createElement("td"); //create a td element
        resultRow.appendChild(trackElement); //add p element to result row

        artistElement = document.createElement("td"); //create a td element
        artistElement.classList.add("artist");
        resultRow.appendChild(artistElement); //add p element to result row

        var stringContent = obj['result'][currentSearch]['tracks'][currentSongArrayPos]["name"];

        for (var artist = 0; artist < obj['result'][currentSearch]['tracks'][currentSongArrayPos]['artists'].length; artist++) {
          if (artist == 0) {
            var stringArtist = obj['result'][currentSearch]['tracks'][currentSongArrayPos]['artists'][artist]['name'];
          }
          else {
            stringArtist += ", " + obj['result'][currentSearch]['tracks'][currentSongArrayPos]['artists'][artist]['name'];
          }
        }

        stringArtist += " - " + obj['result'][currentSearch]['tracks'][currentSongArrayPos]['album']['name'];

        if (recentTracks.indexOf(obj['result'][currentSearch]['tracks'][currentSongArrayPos]['uri']) !== -1) {
          playButton.innerHTML = "✓";
          playButton.setAttribute("disabled", null);
        }
        else {
          playButton.setAttribute("onclick", "playSong(event, '" + obj['result'][currentSearch]['tracks'][currentSongArrayPos]['uri'] + "');" );
          playButton.innerHTML = "Play";
        }

        resultContent = document.createTextNode(stringContent); //add text to textNode object
        artistContent = document.createTextNode(stringArtist);

        trackElement.appendChild(resultContent); //add textnode object to paragraph element
        artistElement.appendChild(artistContent);
        mainTable.appendChild(resultRow); //add rows to table
        resultBox.appendChild(mainTable); //add our completed result div to result box
      }
    }
  }
  if (noResult === true) {
    trackElement = document.createElement("p");
    resultContent = document.createTextNode("No Results Found");
    trackElement.appendChild(resultContent);
    resultBox.appendChild(trackElement);
  }

}
function sendReq () {
  query = document.getElementById('searchArea').value;
  if (query == "") {
    return;
  }

  document.getElementById("resultsCard").style.display = "block";
  var trackElement = document.createElement("p");
  var resultContent = document.createTextNode("Loading...");
  trackElement.appendChild(resultContent);
  var resultsBox = document.getElementById("results");
  resultsBox.innerHTML = null;
  resultsBox.appendChild(trackElement);


  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", reqListener);
  oReq.open("GET", "/action/search.php?q=" + query);
  oReq.send();
}
function playSong(e,uri) {
  var req = new XMLHttpRequest();
  req.addEventListener("load", playListener);
  req.open("GET", "/action/play.php?p=" + uri);
  req.send();

  if ( !e ) e = window.event;

  playButton = e.target;
  playButton.setAttribute("onclick", null );
  playButton.setAttribute("disabled", null);
  playButton.innerHTML = "✓";
}
function playListener() {
  if (this.responseText != "You can't do that.") {
    var obj = JSON.parse(this.responseText);
    console.log(obj);
  }
}
