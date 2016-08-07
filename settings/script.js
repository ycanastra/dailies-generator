function dayStringToNum(day) {
	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
							'Saturday', 'Sunday'];
	return days.indexOf(day);
}

function padHour(hour) {
	var str = hour;
	var pad = '0';
	var ans = pad.substring(0, 1 + pad.length - str.length) + str;
	return ans;
}


$(document).ready(function() {
	$('body').on('click', '.minus', function() {
		removeEntry($(this));
	});
	$('body').on('click', '.plus', function() {
		addNewEntry($(this));
	});
	$('body').on('keydown', 'input', function(event) {
		if (event.keyCode == 13) {
			event.preventDefault();
			var button = $(this).parent().find('button');
			button.click();
			return false;
		}
	})
});

function sort(columnId) {
	tinysort('#' + columnId + ' > div', {selector:'',attr:'id'});
}

function addNewEntry(buttonElement) {
	var div = buttonElement.parent();
	var divId = div.attr('id');
	var columnId = divId.slice(6, divId.length);
	var day = columnId.slice(columnId.length - 1, columnId.length);
	var hourValue = div.find('input[type=number]').val();
	var nameValue = div.find('input[type=text]').val();

	addEntry(columnId, day, hourValue, nameValue);
	removeEmptyEntry(columnId);
	addEmptyEntry(columnId);
}

function removeEntry(buttonElemenmt) {
	var buttonId = buttonElemenmt.attr('id');
	var divId = 'div' + buttonId.slice(1, buttonId.length);
	$('#' + divId).remove();
}

function addEntry(columnId, day, hour, name) {
	var divId = 'div' + columnId + 'h' + padHour(hour);
	var hourId = 'h' + columnId + 'h' + padHour(hour);
	var nameId = 'n' + columnId + 'h' + padHour(hour);
	var buttonId = 'b' + columnId + 'h' + padHour(hour);

	var hourInt = parseInt(hour);

	if($("#" + divId).length != 0) {
		BootstrapDialog.show({
			message: 'Hour ' + hour + ' already exists',
			title: "Error",
			type: BootstrapDialog.TYPE_DANGER
		});
	}
	else if (!hour) {
		BootstrapDialog.show({
			message: 'Please type in an hour',
			title: "Error",
			type: BootstrapDialog.TYPE_DANGER
		});
	}
	else if (!name) {
		BootstrapDialog.show({
			message: 'Please type in a name',
			title: "Error",
			type: BootstrapDialog.TYPE_DANGER
		});
	}
	else if (hourInt < 0 || hourInt > 23) {
		BootstrapDialog.show({
			message: 'Hour ' + hour + ' is not between 0 - 23',
			title: "Error",
			type: BootstrapDialog.TYPE_DANGER
		});
	}
	else {
		var divElem = $('<div id="' + divId + '"></div>')
		var hourInput = $('<input type="number" min="0" max="23" id="' + hourId + '" class="hour">');
		var nameInput = $('<input type="text" id="' + nameId + '" class="name">');
		var minusButton = $('<button id="' + buttonId + '"class="btn btn-danger minus" type="button">-</button>')

		hourInput.val(hour);
		nameInput.val(name);

		hourInput.prop("readonly", true);
		nameInput.prop("readonly", true);

		divElem.append(hourInput);
		divElem.append(nameInput);
		divElem.append(minusButton);

		divElem.appendTo('#' + columnId);
		sort(columnId);

	}
}

function addEmptyEntry(columnId) {
	var hourInput = $('<input type="number" min="0" max="23" class="hour" placeholder="Hour">');
	var nameInput = $('<input type="text" class="name" placeholder="Name">');
	var plusButton = $('<button class="btn btn-default plus" type="button">+</button><br>')

	var div = $('<div class="empty-entry" id="' + 'empty-' + columnId + '"></div>')

	hourInput.appendTo(div)
	nameInput.appendTo(div)
	plusButton.appendTo(div)

	div.appendTo('#' + columnId);
	hourInput.focus();
}

function removeEmptyEntry(columnId) {
	var divId = 'empty-' + columnId;
	var div = $('#' + divId);
	div.remove();
}

$(document).ready(function() {
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

				var columnId = 'col' + locationId + 'day-' + dayStringToNum(day)

				var columnElem = $('<div class="col-md-1" id="' + columnId + '"></div>');
				var dayElem = $('<br><label class="day">' + day + '</label><br>');
				columnElem.appendTo('#' + locationId)
				dayElem.appendTo('#' + columnId);

				$.each(val, function(key, val) {
					addEntry(columnId, day, key, val);
				});
				addEmptyEntry(columnId);
			});
		});
	});
});
