<?php
// Toa Carney 2017

$query = $_GET['p'];

$result = shell_exec("/var/www/radio/scripts/listTracks.sh \"$query\"");

echo($result);
 ?>
