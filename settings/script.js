function dayStringToNum(day) {
	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
							 'Saturday', 'Sunday'];
	return days.indexOf(day);
}

$(document).ready(function() {
	// var next = 1;
	// $(".add-more").click(function(e){
	// 		e.preventDefault();
	// 		var addto = "#field" + next;
	// 		var addRemove = "#field" + (next);
	// 		next = next + 1;
	// 		var newIn = '<input autocomplete="off" class="input form-control" id="field' + next + '" name="field' + next + '" type="text">';
	// 		var newInput = $(newIn);
	// 		var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >-</button></div><div id="field">';
	// 		var removeButton = $(removeBtn);
	// 		$(addto).after(newInput);
	// 		$(addRemove).after(removeButton);
	// 		$("#field" + next).attr('data-source',$(addto).attr('data-source'));
	// 		$("#count").val(next);
	//
	// 				$('.remove-me').click(function(e){
	// 						e.preventDefault();
	// 						var fieldNum = this.id.charAt(this.id.length-1);
	// 						var fieldID = "#field" + fieldNum;
	// 						$(this).remove();
	// 						$(fieldID).remove();
	// 				});
	// });

	var url = 'http://159.203.229.225/dailies_new/data/employee_shifts.json'

	$.getJSON(url, function(data) {
		$.each(data, function(key, val) {
			var locationId = key.split(' ').join('_');
			var newTab = $('<li><a data-toggle="tab" href="#' + locationId + '">' + key + '</a></li>');
			newTab.appendTo('#location-tab');

			var newDiv = $('<div id="' + locationId + '" class="tab-pane fade"></div>');
			var newHeader = $('<h3>' + key + '</h3>');

			newDiv.append(newHeader);
			newDiv.appendTo('#location-tab-content');

			$.each(val, function(key, val) {
				var day = key;

				var columnId = 'col' + locationId + dayStringToNum(day)

				var columnElem = $('<div class="col-md-1" id="' + columnId + '"></div>');
				var dayElem = $('<br><label class="day">' + day + '</label><br>');
				columnElem.appendTo('#' + locationId)
				dayElem.appendTo('#' + columnId);

				console.log(columnId);
				console.log(day);

				$.each(val, function(key, val) {
					var hourId = 'h' + dayStringToNum(day) + key;
					var nameId = 'n' + dayStringToNum(day) + key;
					var buttonId = 'b' + dayStringToNum(day) + key;

					var hourElem = $('<input type="number" min="0" max="23" id="' + hourId + '" class="hour">');
					var nameElem = $('<input type="text" id="' + nameId + '" class="name">');
					var addMoreElem = $('<button id="' + buttonId + '"class="btn btn-danger" type="button">-</button><br>')

					hourElem.val(key);
					nameElem.val(val);

					hourElem.appendTo('#' + columnId);
					nameElem.appendTo('#' + columnId);
					addMoreElem.appendTo('#' + columnId);
				});
			});
		});
	});
});
