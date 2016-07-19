import openpyxl
import datetime
import json
import os

from collections import OrderedDict

from openpyxl.styles import Alignment, Font, Border
from openpyxl.styles.numbers import FORMAT_DATE_TIME1
from openpyxl.styles.borders import Side
from openpyxl.styles.fills import PatternFill
from openpyxl.utils import get_column_letter

class WorkbookCreator:
	def __init__(self, soup, name, group, date, scheduleEvents, workerEvents):
		self.__soup = soup
		self.__name = name
		self.__group = group
		self.__date = date
		self.__scheduleEvents = scheduleEvents
		self.__workerEvents = workerEvents

		self.__wb = openpyxl.Workbook()
		self.__ws = self.__wb.worksheets[0]
		self.__ws.title = group

		self.__noBorder = Border(top=Side(border_style=None),
								 bottom=Side(border_style=None),
								 left=Side(border_style=None),
								 right=Side(border_style=None))
		self.__outsideBorder = Border(top=Side(border_style='medium', color='000000'),
									  bottom=Side(border_style='medium', color='000000'),
									  left=Side(border_style='medium', color='000000'),
									  right=Side(border_style='medium', color='000000'))

		self.__sideBorder = Border(top=Side(border_style=None, color='000000'),
								   bottom=Side(border_style=None, color='000000'),
								   left=Side(border_style='medium', color='000000'),
								   right=Side(border_style='medium', color='000000'))

		self.__bottomBorder = Border(top=Side(border_style=None, color='000000'),
									 bottom=Side(border_style='medium', color='000000'),
									 left=Side(border_style='medium', color='000000'),
									 right=Side(border_style='medium', color='000000'))

		self.__topBorder = Border(top=Side(border_style='medium', color='000000'),
								  bottom=Side(border_style=None, color='000000'),
								  left=Side(border_style='medium', color='000000'),
								  right=Side(border_style='medium', color='000000'))


		self.__whiteFill = PatternFill(fill_type='solid', start_color='FFFFFF')

		self.__yellowFill = PatternFill(fill_type='solid', start_color='FFFF99')

		self.__grayFill = PatternFill(fill_type='solid', start_color='404040')

		self.__centerAlignment = Alignment(horizontal='center', vertical='center',
										   wrap_text=True, shrink_to_fit=False)

		self.getFormatData()

	def generateWorkbook(self):
		group = self.__group
		labLocations = self.getLabLocations()
		employeeLocations = self.getEmployeeLocations()

		currentColumn = 1
		currentRow = 2

		self.createTimeAxis(currentRow, currentColumn)

		currentColumn += 1

		for key, value in labLocations.iteritems():
			self.createLabColumn(currentRow, currentColumn, (key, value))
			currentColumn += 1

		for key, value in employeeLocations.iteritems():
			self.createEmployeeColumn(currentRow, currentColumn, (key, value))
			currentColumn += 1

		self.createTimeAxis(currentRow, currentColumn)

		currentRow = 1
		currentColumn = 1

		self.createHeader(currentRow, currentColumn)

		self.__wb.save(group + '.xlsx')

	def createLabColumn(self, row, col, labNamePair):
		ws = self.__ws
		fontSize = self.__fontSize
		cellWidth = self.__cellWidth

		labNameKey = labNamePair[0] # Lab name that shows up on online labschedule
		labNameValue = labNamePair[1] # Lab name to display on dailies

		scheduleEvents = self.__scheduleEvents

		ws.column_dimensions[get_column_letter(col)].width = cellWidth

		# LabName Title
		currentCell = ws.cell(row=row, column=col)
		currentCell.value = labNameValue
		currentCell.alignment = self.__centerAlignment
		currentCell.font = Font(size=fontSize, bold=True)
		currentCell.border = self.__outsideBorder

		scheduleEvents = [x for x in scheduleEvents if x.getLocation() == labNameKey]

		for item in scheduleEvents:
			if item.getEventName() == labNameKey: # Skip useless scheduleEvent
				continue

			eventName = item.getEventName()
			eventTimeString = item.getTimeString()
			eventTeacher = shortenTeacherName(item.getEventTeacher())

			startTime = item.getStartTime()
			endTime = item.getEndTime()

			startTimeInt = int(startTime.hour) + int(startTime.minute)/60.0
			endTimeInt = int(endTime.hour) + int(endTime.minute)/60.0

			startRow = int((startTimeInt - 8)*2 + row + 1)
			endRow = int((endTimeInt - 8)*2 + row)

			self.setFontSize(startRow, endRow, col, fontSize)
			self.setCenterAlignment(startRow, endRow, col)

			if item.getEventName() == 'OPEN':
				self.setSolidFill(startRow, endRow, col, 'FFFFFF') # White
				self.setBorder(startRow, endRow, col)
				continue
			elif item.getEventName() == 'CLOSED':
				self.setSolidFill(startRow, endRow, col, '404040') # Gray
				self.setBorder(startRow, endRow, col)
				continue
			else: # This is an actual class
				self.setSolidFill(startRow, endRow, col, 'FFFF99') # Yellow
				self.setBorder(startRow, endRow, col)

				# Making sure the event takes up enough cells to merge properly
				if endRow - startRow >= 2:
					self.mergeColumn(startRow, endRow - 2, col)

				ws.cell(row=startRow, column=col).value = eventName

				if startRow != endRow: # If the event takes up more than one cell
					ws.cell(row=endRow, column=col).value = eventTimeString

					for i in range(startRow + 1, endRow):
						if i == endRow - 1:
							ws.cell(row=i, column=col).value = eventTeacher

	def createEmployeeColumn(self, row, col, employeeLocationPair):
		ws = self.__ws
		fontSize = self.__fontSize
		cellWidth = self.__cellWidth
		workerEvents = self.__workerEvents
		day = (self.__date.weekday() + 1)%7

		# Employee location names that are contained in ./data/employee_shifts/*
		employeeLocationKey = employeeLocationPair[0]
		# Employee location name that is displayed on the dailies
		employeeLocationValue = employeeLocationPair[1]

		ws.column_dimensions[get_column_letter(col)].width = cellWidth

		# employeeLocation Title
		currentCell = ws.cell(row=row, column=col)
		currentCell.value = employeeLocationValue
		currentCell.alignment = self.__centerAlignment
		currentCell.font = Font(size=fontSize, bold=True)
		currentCell.border = self.__outsideBorder

		workerEvents = [x for x in workerEvents if x.getDay() == day]
		workerEvents = [x for x in workerEvents if x.getLocation() == employeeLocationKey]

		for item in workerEvents:
			name = item.getName()
			timeString = item.getTimeString()

			startTime = item.getStartTime()
			endTime = item.getEndTime()

			startTimeInt = int(startTime.hour) + int(startTime.minute)/60.0
			endTimeInt = int(endTime.hour) + int(endTime.minute)/60.0

			startRow = int((startTimeInt - 8)*2 + row + 1)
			endRow = int((endTimeInt - 8)*2 + row)

			ws.cell(row=startRow, column=col).value = name
			ws.cell(row=endRow, column=col).value = timeString

			self.setBorder(startRow, endRow, col)
			self.setCenterAlignment(startRow, endRow, col)
			self.setFontSize(startRow, endRow, col, fontSize)
			self.setSolidFill(startRow, endRow, col, 'FFFFFF') # White

			self.setBorder(endRow + 1, ws.max_row, col)
			self.setCenterAlignment(endRow + 1, ws.max_row, col)
			self.setFontSize(endRow + 1, ws.max_row, col, fontSize)
			self.setSolidFill(endRow + 1, ws.max_row, col, '404040') # Gray

	def createTimeAxis(self, row, col):
		ws = self.__ws
		timeCellWidth = self.__timeCellWidth
		cellHeight = self.__cellHeight
		fontSize = self.__fontSize

		self.addTimeTitle(row, col)

		ws.column_dimensions[get_column_letter(col)].width = timeCellWidth

		for i in xrange(0, 29):
			currentRow = row + i + 1
			currentCell = ws.cell(row=currentRow, column=col)

			ws.row_dimensions[currentRow].height = cellHeight

			if i%2 == 0:
				currentCell.value = datetime.datetime.strptime(str(i/2 + 8), '%H')

			currentCell.number_format = FORMAT_DATE_TIME1
			currentCell.font = Font(size=fontSize)
			currentCell.fill = self.__whiteFill

			if i == 0:
				currentCell.border = self.__topBorder
			elif i == 28:
				currentCell.border = self.__bottomBorder
			else:
				currentCell.border = self.__sideBorder


	def createHeader(self, row, col):
		ws = self.__ws
		name = 'Name: ' + self.__name
		group = self.__group

		headerHeight = self.__headerHeight
		headerFontSize = self.__headerFontSize

		title = 'Collaborate Student Support Center ' + group

		maxCol = ws.max_column
		maxTitleCol = maxCol*2/3

		self.mergeRow(row, col, maxTitleCol)
		self.mergeRow(row, maxTitleCol + 1, maxCol)

		ws.cell(row=row, column=col).value = title
		ws.cell(row=row, column=maxTitleCol + 1).value = name

		ws.row_dimensions[row].height = headerHeight

		ws.cell(row=row, column=col).font = Font(size=headerFontSize, bold=True)
		ws.cell(row=row, column=maxTitleCol + 1).font = Font(size=headerFontSize, bold=True)

		self.setCenterAlignment(row, row, col)
		self.setCenterAlignment(row, row, maxTitleCol + 1)


	def getEmployeeLocations(self):
		group = self.__group
		path = './data/group_data.json'

		file = open(path)
		data = json.load(file, object_pairs_hook=OrderedDict)

		return data[group]['Employee Locations']

	def getLabLocations(self):
		group = self.__group
		path = './data/group_data.json'

		file = open(path)
		data = json.load(file, object_pairs_hook=OrderedDict)

		return data[group]['Labs']


	def getFormatData(self):
		group = self.__group
		path = './data/group_data.json'

		file = open(path)
		data = json.load(file)
		data = data[group]['Worksheet Format']

		self.__cellHeight = data['cell_height']
		self.__cellWidth = data['cell_width']
		self.__fontSize = data['font_size']
		self.__timeCellWidth = data['time_cell_width']
		self.__headerHeight = data['header_height']
		self.__headerFontSize = data['header_font_size']

	def setBorder(self, startRow, endRow, column):
		ws = self.__ws
		if startRow == endRow:
			ws.cell(row=startRow, column=column).border = self.__outsideBorder
		else:
			ws.cell(row=startRow, column=column).border = self.__topBorder
			ws.cell(row=endRow, column=column).border = self.__bottomBorder

			for i in range(startRow + 1, endRow):
				ws.cell(row=i, column=column).border = self.__sideBorder

	def setSolidFill(self, startRow, endRow, column, color):
		ws = self.__ws
		patternFill = PatternFill(fill_type='solid', start_color=color)
		for i in range(startRow, endRow + 1):
			ws.cell(row=i, column=column).fill = patternFill

	def setFontSize(self, startRow, endRow, column, fontSize):
		ws = self.__ws
		for i in range(startRow, endRow + 1):
			ws.cell(row=i, column=column).font = Font(size=fontSize)

	def setCenterAlignment(self, startRow, endRow, column):
		ws = self.__ws
		for i in range(startRow, endRow + 1):
			ws.cell(row=i, column=column).alignment = self.__centerAlignment

	def mergeColumn(self, startRow, endRow, column):
		ws = self.__ws

		ws.merge_cells(start_row=startRow, start_column=column, end_row=endRow,
					   end_column=column)

	def mergeRow(self, row, startCol, endCol):
		ws = self.__ws

		ws.merge_cells(start_row=row, start_column=startCol, end_row=row,
					   end_column=endCol)

	def addTimeTitle(self, row, col):
		ws = self.__ws
		fontSize = self.__fontSize
		cellHeight = self.__cellHeight

		ws.row_dimensions[row].height = cellHeight

		timeCell = ws.cell(row=row, column=col)
		timeCell.value = 'Time'
		timeCell.alignment = self.__centerAlignment
		timeCell.font = Font(size=fontSize, bold=True)
		timeCell.border = self.__outsideBorder

def shortenTeacherName(teacherName):
	if teacherName == 'To Be Determined':
		return 'TBD'
	elif teacherName == None:
		return None
	else:
		return teacherName
