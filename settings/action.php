<?php
	// header('Content-type: application/json');
	// phpinfo();
	// echo "hello\n";
	$json = $_POST['json'];

	$json = json_encode($json);

	$file = fopen('test.txt','w+');
	fwrite($file, $json);
	fclose($file);
	echo $json;
	// echo 'success?';
?>
