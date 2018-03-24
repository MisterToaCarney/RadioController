<!DOCTYPE html>
<!--
Written by Toa Carney 2018

Stop snooping around, thx.
-->
<html>
<head>
  <title>Flex FM - Info</title>
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
              <li><a class="active">Info</a></li>
            </ul>
          </nav>
        </div>
      </header>

      <script type="text/javascript" src="/js/nowPlaying.js"></script>
      <script type="text/javascript" src="/js/websocket.js"></script>

      <div class="body">
        <div class="card">
          <h1 id="flex-fm---info">Flex FM - Info</h1>
          <h2 id="overview">Overview</h2>
          <p>Flex FM is a low powered radio station based in the Roslyn Area of Palmerston North, New Zealand. It plays a reasonably wide variety of music.</p>
          <h2 id="concept">Concept</h2>
          <p>Flex FM is a community driven initiative. A key component of the Flex FM system is the ability for listeners to play their choice of tracks on the radio. As a result, the music that plays on Flex FM is a direct reflection of the community behind it. <strong>Anyone</strong> has the ability to play a track on Flex FM.</p>
          <h2 id="how-it-works">How it Works</h2>
          <p>Flex FM runs and operates with full autonomy using free and open-source software. Users can request tracks by searching for them on the <a href="https://www.flexfm.org/">Flex FM website</a>. The system orders requests in a track queue and plays them one by one.</p>
          <h2 id="how-to-listen">How to Listen</h2>
          <p>There are two ways to listen to Flex FM:</p>
            <ol>
              <li>Via an FM radio</li>
              <li>Via an Internet Stream</li>
            </ol>
          <h3 id="internet-stream">Internet Stream</h3>
          <p>Flex FM operates an internet stream available at the <a href="http://flexfm.org/stream/">Flex FM website</a>.</p>
          <p>The Flex FM internet stream uses open source codecs and is delivered by HTTP. As a result, the stream can be played back on virtually any device connected to the internet without the need for additional software.</p>
          <h3 id="fm-radio-link">FM Radio Link</h3>
          <p>Flex FM broadcasts on <strong>88.3MHz</strong> in the Roslyn/Freyberg area of Palmerston North. This frequency is allocated as a part of the <em>Low Power FM broadcast band</em> (LPFM). This band is designed to allow unlicensed FM broadcasts within a limited radius. Additional information regarding LPFM broadcasting can be found at <a href="https://www.rsm.govt.nz/about-rsm/spectrum-policy/gazette/gurl/low-power-fm-broadcasting">Radio Spectrum Management NZ</a>.</p>
          <p>Given the location of Flex FM, the LPFM band is very crowded. This is problematic when trying to listen from some areas of Palmerston North. If you are having issues hearing Flex FM via radio, the internet stream may be a better choice.</p>
        </div>
        <div class="card">
          <h1>Diagrams</h1>
          <img width="100%" src="overview.svg" alt="Block Diagram of Flex FM">
        </div>
      </div>



      <footer>
        <div class="footer-cont">
          <p>Flex FM</p>
        </div>
      </footer>

    </body>
    </html>
