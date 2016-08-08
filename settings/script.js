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

namesList = []

$(document).ready(function() {
	init();
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
	});
	$('#save-button').on('click', function(event) {
		event.preventDefault();
		createJSON();
		return false;
	});
	$('#revert-button').on('click', function(event) {
		event.preventDefault();
		location.reload();
		return false;
	});
});

function createJSON() {
	var locations = []
	var json = {}
	$('div').each(function() {
		if ($(this).hasClass('tab-pane')) {
			var locationName = $(this).find('h3').html();
			var columns = $(this).find('.col-md-1');
			json[locationName] = {};
			$.each(columns, function(index, columnDiv) {
				var day = $(columnDiv).find('label').html();
				var entries = $(columnDiv).find('div');
				json[locationName][day] = {};
				$.each(entries, function(index, entry) {
					if (!$(entry).hasClass('empty-entry')) {
						var hourInput = $(entry).find('input[type=number]')
						var nameInput = $(entry).find('input[type=text]')

						var hourVal = hourInput.val();
						var nameVal = nameInput.val();

						json[locationName][day][hourVal] = nameVal;
					}
				});
			});
		}
	});

	var pathname = window.location.pathname;

	$.ajax({
			url: pathname + 'action.php',
			type: 'POST',
			data: {'json': json},
			success: function() {
				console.log('success i guess?');
			},
			error: function(e){
				console.log('error i guess?');
			}
	});
}

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
		var minusButton = $('<button id="' + buttonId + '"class="btn btn-danger minus" type="button">-</button>');

		hourInput.val(hour);
		nameInput.val(name);

		hourInput.prop("readonly", true);
		nameInput.prop("readonly", true);

		divElem.append(hourInput);
		divElem.append(nameInput);
		divElem.append(minusButton);

		divElem.appendTo('#' + columnId);
		sort(columnId);

		if (namesList.indexOf(name) == -1) {
			namesList.push(name);
		}
	}
}

function addPlusTab() {
	var newTab = $('<li><a data-toggle="tab" href="#">' + '+' + '</a></li>');
	newTab.appendTo('#location-tab');

	// var newDiv = $('<div id="' + locationId + '" class="tab-pane fade"></div>');
	// var newHeader = $('<h3>' + key + '</h3>');

	// newDiv.append(newHeader);
	// newDiv.appendTo('#location-tab-content');
}

function addEmptyEntry(columnId) {
	var hourInput = $('<input type="number" min="0" max="23" class="hour" placeholder="Hour" list="names-list">');
	var nameInput = $('<input type="text" class="name" placeholder="Name">');
	var plusButton = $('<button class="btn btn-default plus" type="button">+</button><br>');

	var div = $('<div class="empty-entry" id="' + 'empty-' + columnId + '"></div>');

	nameInput.typeahead({
		source: namesList,
		fitToElement: true
	});

	hourInput.appendTo(div);
	nameInput.appendTo(div);
	plusButton.appendTo(div);

	div.appendTo('#' + columnId);
	hourInput.focus();
}

function removeEmptyEntry(columnId) {
	var divId = 'empty-' + columnId;
	var div = $('#' + divId);
	div.remove();
}

function init() {
	var pathname = window.location.pathname;
	var url = '../data/employee_shifts.json'
	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

	var names = []

	$.getJSON(url, function(data) {
		$.each(data, function(key, val) {
			var locationId = key.split(' ').join('_');
			var newTab = $('<li><a data-toggle="tab" href="#' + locationId + '">' + key + '</a></li>');
			newTab.appendTo('#location-tab');

			var newDiv = $('<div id="' + locationId + '" class="tab-pane fade"></div>');
			var newHeader = $('<h3>' + key + '</h3>');

			newDiv.append(newHeader);
			newDiv.appendTo('#location-tab-content');

			for (var i = 0; i < days.length; i++) {
				var day = days[i];
				var columnId = 'col' + locationId + 'day-' + dayStringToNum(day);

				var columnElem = $('<div class="col-md-1" id="' + columnId + '"></div>');
				var dayElem = $('<br><label class="day">' + day + '</label><br>');
				columnElem.appendTo('#' + locationId);
				dayElem.appendTo('#' + columnId);

				if (val[day] != undefined) {
					$.each(val[day], function(key, val) {
						addEntry(columnId, day, key, val);
					});
				}
				addEmptyEntry(columnId);
			}
		});

		$('input[type=text]').typeahead({
			source: names
		});
		addPlusTab()
	});

	// for (let item of names) {
	// 	console.log(item);
	// }
	// console.log(names.has('Emily'));
	//
	// for (let item of names) {
	// 	console.log(item);
	// }
	//
	// for (var i = 0; i < names.length; i++) {
	// 	console.log(names[i]);
	// 	var nameOption = $('<option value="' + names[i] + '" />');
	// 	nameOption.appendTo('#names-list');
	// }
}
