<!DOCTYPE html>
<!--
Written by Toa Carney 2017

Stop snooping around, thx.
-->
<html>
<head>
  <title>Radio</title>
  <meta name="viewport" content="width=device-width, initial-scale=0.9">
  <link href="style.css" rel="stylesheet">
</head>

<body>
  <header>
    <div class="header-cont">
      <h1 class="main">Flex FM</h1>
      <h2 class="main">Track Player - Version 0.4.1</h2>

      <nav>
        <ul>
          <li><a>Home</a></li>
          <li><a>Info</a></li>
        </ul>
      </nav>
    </div>
  </header>

<div class="body">

  <div class="card">
      <h3>Now Playing</h3>
      <p>Title: <span id="trackName">Nothing!</span></p>
      <p>Artist:  <span id="artistName"></span></p>
      <p>Album: <span id="albumName"></span></p>
    </div>

    <script type="text/javascript">
    function toggleQ() {
      q = document.getElementById("queue");
      if (q.style.display == "block") {
        q.style.display = "none";      
      }
      else {
        q.style.display = "block";
      }
    }


    </script>
    <div class="card">
      <h3>Track Queue</h3>
      <button class="queue" onclick="toggleQ()">Show</button>
      <div class="queue" id="queue">
        <p>Error: No queue info.</p>
      </div>
    </div>

    <script type="text/javascript">
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
          text = document.createTextNode(trackList['result'][i]['artists'][0]['name'] + " - " + trackList['result'][i]['name'])
          element = document.createElement('li');

          element.appendChild(text);
          listElement.appendChild(element);
        }
      }
      else {
        listDiv.innerHTML = "<p>No Tracks In Queue</p>"
      }
    }

    </script>







  <script type="text/javascript">
  var track;
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", requestListener);
  oReq.open("GET", "/action/get_track.php");
  oReq.send();

  function requestListener() {
    track = JSON.parse(this.responseText);
    console.log(track);
    document.getElementById("trackName").innerHTML = "";
    document.getElementById("artistName").innerHTML = "";
    document.getElementById("albumName").innerHTML = "";

    document.getElementById("trackName").appendChild(document.createTextNode(track['result']['name']));

    for (var i = 0; i < track['result']['artists'].length; i++) {
      if (i == 0) {
        document.getElementById("artistName").appendChild(document.createTextNode(track['result']['artists'][i]['name']));
      }
      else {
        document.getElementById("artistName").appendChild(document.createTextNode(", " + track['result']['artists'][i]['name']));
      }
    }
    document.getElementById("albumName").appendChild(document.createTextNode(track['result']['album']['name']));
  }

  var centralController = new WebSocket("wss://" + location.host + ":8000");

  centralController.onmessage = function (event) {
    console.log(event.data);
    msg = JSON.parse(event.data);
    console.log(msg);

    if (msg['event'] == "track_playback_started") {

      document.getElementById("trackName").innerHTML = "";
      document.getElementById("artistName").innerHTML = "";
      document.getElementById("albumName").innerHTML = "";


      document.getElementById("trackName").appendChild(document.createTextNode(msg['tl_track']['track']['name']));

      for (var i = 0; i < msg['tl_track']['track']['artists'].length; i++) {
        if (i == 0) {
          document.getElementById("artistName").appendChild(document.createTextNode(msg['tl_track']['track']['artists'][i]['name']));
        }
        else {
          document.getElementById("artistName").appendChild(document.createTextNode(", " + msg['tl_track']['track']['artists'][i]['name']));
        }
      }
      document.getElementById("albumName").appendChild(document.createTextNode(msg['tl_track']['track']['album']['name']));

    }
    else if (msg['id'] == "getTL") {
      trackList = msg;
      listDiv = document.getElementById("queue");
      listDiv.innerHTML = "";

      listElement = document.createElement('ol');
      listDiv.appendChild(listElement);
      if (trackList['result'].length > 1) {
        for (var i = 1; i < trackList['result'].length; i++) {
          text = document.createTextNode(trackList['result'][i]['artists'][0]['name'] + " - " + trackList['result'][i]['name'])
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
  </script>

  <hr>
  <form action="javascript:void(0);">
   <input type="text" id="searchArea" placeholder="Search Music">
   <input type="submit" onclick="sendReq()" value="Search">
 </form>
 <div id="results">
 </div>


 <script>
 function reqListener () {
  var currentSongArrayPos;
  var currentSearch;
  var noResult = true;

  obj = JSON.parse(this.responseText);
  console.log(obj);
  var resultBox = document.getElementById("results");
  resultBox.innerHTML = null;

  var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/scripts/recentTracks.txt", false ); // false for synchronous request
    xmlHttp.send( null );

    var recentTracks = xmlHttp.responseText;

    for (currentSearch = 0; currentSearch < obj['result'].length; currentSearch++) {

      if (typeof obj['result'][currentSearch]['tracks'] != 'undefined') {
        noResult = false;
        for (currentSongArrayPos = 0; currentSongArrayPos < obj['result'][currentSearch]['tracks'].length; currentSongArrayPos++) {
          resultDiv = document.createElement("div"); //create our result div
          resultDiv.classList.add("result"); //add class 'result' to our result div

          playButton = document.createElement('button'); //create button
          resultDiv.appendChild(playButton); //add playbutton to result div

          trackElement = document.createElement("p"); //create a paragraph element
          resultDiv.appendChild(trackElement); //add p element to result div

          artistElement = document.createElement("p"); //create a paragraph element
          artistElement.classList.add("artist");
          resultDiv.appendChild(artistElement); //add p element to result div

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
          resultBox.appendChild(resultDiv); //add our completed result div to result box
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
  </script>
</div>

<footer>
  <div class="footer-cont">
    <p>Flex FM</p>
  </div>
</footer>

</body>
</html>
