
$("#submit").prop("disabled", true);

$("input[name=name]").on("change", function() {
	if ($(this).val().length > 0 && $("input[name=date]").val().length > 0) {
		$("#submit").prop("disabled", false);
	}
	else {
		$("#submit").prop("disabled", true);
	}
});

$("input[name=date]").on("change", function() {
	if ($(this).val().length > 0 && $("input[name=name]").val().length > 0) {
		$("#submit").prop("disabled", false);
	}
	else {
		$("#submit").prop("disabled", true);
	}
});
