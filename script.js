$(document).ready(function() {
	buttonEnabler();
})

$('p.errorMessage').hide();

$('input').on('input change', buttonEnabler);
$('select').on('change', buttonEnabler);

$('select').blur(function() {
	if ($(this).val() == null) {
		showError($(this));
	}
	else {
		hideError($(this));
	}
})

$('input').on('input change', function() {
	if ($(this).val() != '') {
		hideError($(this));
	}
});

$('input').not('#datepicker').blur(function() {
	if ($(this).val() == '') {
		showError($(this));
	}
});

$('#datepicker').datepicker({
	autoclose: true
}).on('hide', function(event) {
	var dateText = event.format('mm/dd/yyyy');
	if (dateText == '') {
		showError($(this));
	}
	else {
		hideError($(this));
	}
});

function hideError(input) {
	input.parent().find('p').hide();
	input.css('border', '');
}

function showError(input) {
	input.parent().find('p').show();
	input.css('border', '1px solid red');
}

function buttonEnabler() {
	var inputEmpty = false;
	var selectEmpty = false;

	$('input').each(function() {
		if ($(this).val() == '') {
			inputEmpty = true;
		}
	});

	$('select').each(function() {
		if ($(this).val() == null) {
			selectEmpty = true;
		}
	});

	if (inputEmpty || selectEmpty) {
		$('#submit').prop("disabled", true);
	}
	else {
		$('#submit').prop("disabled", false);
	}
}
