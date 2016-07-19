<?php

	$name = addslashes($_POST['name']);
	$group = addslashes($_POST['group']);
	$date = addslashes($_POST['date']);

	$filename = $group .'.xlsx';

	$name = escapeshellarg($name);
	$group = escapeshellarg($group);

	$output = shell_exec('python ./py/main.py ' .$name .' ' .$group .' ' .$date);
	header('Location: http://159.203.229.225/dailies_new/' .$filename);

?>
