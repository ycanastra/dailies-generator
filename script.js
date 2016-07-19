
$("#submit").prop("disabled", true);

// $("input[name=name]").on("change", function() {
// 	if ($(this).val().length > 0 && $("input[name=date]").val().length > 0) {
// 		$("#submit").prop("disabled", false);
// 	}
// 	else {
// 		$("#submit").prop("disabled", true);
// 	}
// });
//
// $("input[name=date]").on("change", function() {
// 	if ($(this).val().length > 0 && $("input[name=name]").val().length > 0) {
// 		$("#submit").prop("disabled", false);
// 	}
// 	else {
// 		$("#submit").prop("disabled", true);
// 	}
// });

// function buttonEnabler(inputEmpty)

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
	} else {
		$('#submit').prop("disabled", false)
	}
}
