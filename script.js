$("#submit").prop("disabled", true)
$('p.errorMessage').hide()

$('input').on('input change', buttonEnabler)
$('select').on('change', buttonEnabler)

$('select').on('change', function() {
	if ($(this).val() != null) {
		$(this).parent().find('p').slideUp(150)
		$(this).css('border', '')	
	}
})

$('input').on('input change', function() {
	if ($(this).val() != '') {
		$(this).parent().find('p').slideUp(150)
		$(this).css('border', '')
	}
})

$('input').not('#datepicker').blur(function() {
	if ($(this).val() == '') {
		$(this).css('border', '1px solid red')
		$(this).parent().find('p').slideDown(150)
	}
})

$('#datepicker').datepicker({
  onClose: function(dateText) {
		if (dateText == '') {
			$(this).css('border', '1px solid red')
			$(this).parent().find('p').slideDown(150)
		}
		else {
			$(this).parent().find('p').slideUp(150)
		  $(this).css('border', '')
		}
	}
})

$('select').blur(function() {
	if ($(this).val() == null) {
		$(this).css('border', '1px solid red')
		$(this).parent().find('p').slideDown(150)
	}
})

function buttonEnabler() {
	var inputEmpty = false
	var selectEmpty = false

	$('input').each(function() {
		if ($(this).val() == '') {
			inputEmpty = true
		}
	})

	$('select').each(function() {
		if ($(this).val() == null) {
			selectEmpty = true
		}
	})

	if (inputEmpty || selectEmpty) {
		$('#submit').prop("disabled", true)
	}
	else {
		$('#submit').prop("disabled", false)
	}
}
