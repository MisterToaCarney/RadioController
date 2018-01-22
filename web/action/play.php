<?php
// Toa Carney 2017

$query = $_GET['p'];
$recent = file_get_contents("/var/www/radio/scripts/recentTracks.txt");

if ( strpos($recent, $query) === FALSE && substr($query, 0, 14) === "spotify:track:") {
	$result = shell_exec("/var/www/radio/scripts/play.sh \"$query\"");
	echo($result);
}
else if (strpos($recent, $query) === FALSE && substr($query, 0, 16) === "soundcloud:song/") {
	$result = shell_exec("/var/www/radio/scripts/play.sh \"$query\"");
        echo($result);
}
else {
	echo("You can't do that.");
}

 ?>
