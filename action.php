<?php

	$name = addslashes($_POST['name']);
	$group = addslashes($_POST['group']);
	$date = addslashes($_POST['date']);

	$filename = $group .'.xlsx';

	$name = escapeshellarg($name);
	$group = escapeshellarg($group);

	exec('python ./py/main.py ' .$name .' ' .$group .' ' .$date, $output, $return);

	if ($return == 0) {
		header('Location: http://159.203.229.225/dailies_new/' .$filename);
	}
	else {
		echo "The program failed to run. Please go back and try again.";
	}
	
?>
