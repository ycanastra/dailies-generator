$("#submit").prop("disabled", true);

$('form > input').on('input change', buttonEnabler);
$('form > select').on('change', buttonEnabler);

function buttonEnabler() {
	var inputEmpty = false;
	var selectEmpty = false;

	$('form > input').each(function() {
		if ($(this).val() == '') {
			inputEmpty = true;
		}
	});

	$('form > select').each(function() {
		if ($(this).val() == null) {
			selectEmpty = true;
		}
	});

	if (inputEmpty || selectEmpty) {
		$('#submit').prop("disabled", true)
	}
	else {
		$('#submit').prop("disabled", false)
	}
}
