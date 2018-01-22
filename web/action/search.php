<?php
// Toa Carney 2017

$query = $_GET['q'];

$result = shell_exec("/var/www/radio/scripts/search.sh \"$query\"");

echo($result);

 ?>
