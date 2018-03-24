<!DOCTYPE html>
<!--
Written by Toa Carney 2017

Stop snooping around, thx.
-->
<html>
<head>
  <title>Radio</title>
  <meta name="google-site-verification" content="Kl1I_amczYSsOtEQW8WURk3xV_jtTjGCd0foAF1aeWU" />
  <meta name="viewport" content="width=device-width, initial-scale=0.9">
  <link href="/style.css" rel="stylesheet">
</head>

<body>
  <header>
    <div class="header-content">

      <div class="lr-container">
        <div class="left">
          <h1>Flex FM</h1>
        </div>
        <div class="right">
          <h2>Now Playing</h2>
          <p class="now-playing-meta"></p>
          <audio controls>
            <source src="http://stream.flexfm.org:8000/flexfm.ogg" type="audio/ogg">
        </div>
      </div>

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
      <h2>Now Playing</h2>
      <p>Title: <span id="trackName">Connecting to Station...</span></p>
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
      <div class="lr-container">
        <h2 class="left">Track Queue</h2>
        <button class="queue right" onclick="toggleQ()">Show</button>
      </div>
      <div class="queue" id="queue">
        <p>Connecting to Station...</p>
      </div>
    </div>

    <script type="text/javascript" src="/js/tracklist.js"></script>
    <script type="text/javascript" src="/js/nowPlaying.js"></script>
    <script type="text/javascript" src="/js/websocket.js"></script>

    <hr>
    <form action="javascript:void(0);">
      <input type="text" id="searchArea" placeholder="Search Music">
      <input type="submit" onclick="sendReq()" value="Search">
    </form>
    <div id="resultsCard" class="card">
    <h2>Results</h2>
    <div id="results">
    </div>
    </div>
    <script type="text/javascript" src="/js/request.js"></script>
  </div>

  <footer>
    <div class="footer-cont">
      <p>Flex FM</p>
    </div>
  </footer>

</body>
</html>
