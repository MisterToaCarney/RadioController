<?php
// Toa Carney 2017

function getRealIpAddr() {
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
      $ip = $_SERVER['HTTP_CLIENT_IP'];
    }
    else if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
      $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    }
    else {
      $ip = $_SERVER['REMOTE_ADDR'];
    }
    return($ip);
}

function removeLinePos($needle, $haystack) {
  $lines = explode("\n", $haystack);
	$output = array();
	foreach ($lines as $line) {
		if (strpos($line, $needle) === FALSE) {
			$output[] = $line;
		}
	}
	return(implode("\n", $output));
}

$query = $_GET['p'];
$recent = file_get_contents("../scripts/recentTracks.txt");

if (strpos($recent, $query) === FALSE && substr($query, 0, 14) === "spotify:track:") {

	$ip = getRealIpAddr();
	$currentTime = time();

	$oldFile = file_get_contents("requests.csv");
	$lines = explode("\n", $oldFile);
	foreach ($lines as $line) {
		$cells = explode(",", $line);
		if ($cells[0] === $ip) {
			$diff = $currentTime - $cells[1];
			if ($diff < 300) {
				exit("Too early. $diff");
			}
		}
	}
	$newFile = removeLinePos($ip.",", $oldFile);
	file_put_contents("requests.csv", $newFile);
	file_put_contents("requests.csv", $ip.",".$currentTime."\n", FILE_APPEND);

	$result = shell_exec("../scripts/play.sh \"$query\"");
	echo($result);
}
/*else if (strpos($recent, $query) === FALSE && substr($query, 0, 16) === "soundcloud:song/") {
	$result = shell_exec("../scripts/play.sh \"$query\"");
        echo($result);
}*/
else {
	echo("You can't do that.");
}

 ?>
