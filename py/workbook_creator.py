import openpyxl
import datetime
import json
import os

from workbook_formatter import WorkbookFormatter

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

		self.__wf = WorkbookFormatter(self.__ws, self.__group)

	# TODO use font in group_data.json
	def generateWorkbook(self):
		group = self.__group
		labLocations = self.getLabLocations()
		employeeLocations = self.getEmployeeLocations()

		currentColumn = 1
		currentRow = 2

		self.createTimeColumn(currentRow, currentColumn)
		currentColumn += 1

		for key, value in labLocations.iteritems():
			self.createLabColumn(currentRow, currentColumn, (key, value))
			currentColumn += 1

		for key, value in employeeLocations.iteritems():
			self.createEmployeeColumn(currentRow, currentColumn, (key, value))
			currentColumn += 1

		self.createTimeColumn(currentRow, currentColumn)
		currentColumn += 1

		self.createNotesColumn(currentRow, currentColumn)

		currentRow = 1
		currentColumn = 1

		self.createTitle(currentRow, currentColumn)

		self.__wb.save(group + '.xlsx')

	def createLabColumn(self, row, col, labNamePair):
		ws = self.__ws
		wf = self.__wf
		fontSize = wf.labFontSize
		cellWidth = wf.labCellWidth

		labNameKey = labNamePair[0] # Lab name that shows up on online labschedule
		labNameValue = labNamePair[1] # Lab name to display on dailies

		scheduleEvents = self.__scheduleEvents

		ws.column_dimensions[get_column_letter(col)].width = cellWidth

		# LabName Title
		self.createHeader(row, col, labNameValue)

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

			wf.setFontSize(startRow, endRow, col, col, fontSize)
			wf.setCenterAlignment(startRow, endRow, col, col)

			if item.getEventName() == 'OPEN':
				# self.setSolidFill(startRow, endRow, col, 'FFFFFF') # White

				# patternFill = PatternFill(fill_type='solid', start_color=color)
				for i in range(startRow, endRow + 1):
					if (i + 1)%4 < 2:
						ws.cell(row=i, column=col).fill = wf.whiteFill
					else:
						ws.cell(row=i, column=col).fill = wf.lightgrayFill

				wf.setBorder(startRow, endRow, col, col)
				continue
			elif item.getEventName() == 'CLOSED':
				wf.setSolidFill(startRow, endRow, col, col, '404040') # Gray
				wf.setBorder(startRow, endRow, col, col)
				continue
			else: # This is an actual class
				wf.setSolidFill(startRow, endRow, col, col, 'FFFFFF') # Yellow
				wf.setBorder(startRow, endRow, col, col)

				# Making sure the event takes up enough cells to merge properly
				if endRow - startRow >= 2:
					wf.setMerge(startRow, endRow - 2, col, col)

				ws.cell(row=startRow, column=col).value = eventName

				if startRow != endRow: # If the event takes up more than one cell
					ws.cell(row=endRow, column=col).value = eventTimeString

					for i in range(startRow + 1, endRow):
						if i == endRow - 1:
							ws.cell(row=i, column=col).value = eventTeacher

	def createEmployeeColumn(self, row, col, employeeLocationPair):
		ws = self.__ws
		wf = self.__wf
		fontSize = wf.employeeFontSize
		cellWidth = wf.employeeCellWidth
		workerEvents = self.__workerEvents
		day = (self.__date.weekday() + 1)%7

		# Employee location names that are contained in ./data/employee_shifts/*
		employeeLocationKey = employeeLocationPair[0]
		# Employee location name that is displayed on the dailies
		employeeLocationValue = employeeLocationPair[1]

		ws.column_dimensions[get_column_letter(col)].width = cellWidth

		# employeeLocation Title
		self.createHeader(row, col, employeeLocationValue)

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

			wf.setBorder(startRow, endRow, col, col)
			wf.setCenterAlignment(startRow, endRow, col, col)
			wf.setFontSize(startRow, endRow, col, col, fontSize)
			wf.setSolidFill(startRow, endRow, col, col, 'FFFFFF') # White

			wf.setBorder(endRow + 1, ws.max_row, col, col)
			wf.setCenterAlignment(endRow + 1, ws.max_row, col, col)
			wf.setFontSize(endRow + 1, ws.max_row, col, col, fontSize)
			wf.setSolidFill(endRow + 1, ws.max_row, col, col, '404040') # Gray

	def createTimeColumn(self, row, col):
		ws = self.__ws
		wf = self.__wf
		cellWidth = wf.timeCellWidth
		cellHeight = wf.cellHeight
		fontSize = wf.timeFontSize

		self.createHeader(row, col, 'Time')

		ws.column_dimensions[get_column_letter(col)].width = cellWidth
		wf.setTopAlignment(row + 1, row + 29, col, col)

		for i in xrange(0, 29):
			currentRow = row + i + 1
			currentCell = ws.cell(row=currentRow, column=col)

			ws.row_dimensions[currentRow].height = cellHeight

			if i%2 == 0:
				currentCell.value = datetime.datetime.strptime(str(i/2 + 8), '%H')

			currentCell.number_format = FORMAT_DATE_TIME1
			currentCell.font = Font(size=fontSize)
			if (currentRow + 1)%4 < 2:
				currentCell.fill = wf.whiteFill
			else:
				currentCell.fill = wf.lightgrayFill

		wf.setBorder(row + 1, row + 29, col, col)
		
	def createNotesColumn(self, row, col):
		ws = self.__ws
		wf = self.__wf
		cellWidth = wf.notesCellWidth

		self.createHeader(row, col, 'Notes')

		ws.column_dimensions[get_column_letter(col)].width = cellWidth

		for i in xrange(0, 29):
			currentRow = row + i + 1
			currentCell = ws.cell(row=currentRow, column=col)

			if (currentRow + 1)%4 < 2:
				currentCell.fill = wf.whiteFill
			else:
				currentCell.fill = wf.lightgrayFill

			if i == 0:
				currentCell.border = wf.topBorder
			elif i == 28:
				currentCell.border = wf.bottomBorder
			else:
				currentCell.border = wf.sideBorder

	def createHeader(self, row, col, headerText):
		ws = self.__ws
		wf = self.__wf
		fontSize = wf.headerFontSize
		cellHeight = wf.headerCellHeight
		group = self.__group

		ws.row_dimensions[row].height = cellHeight

		timeCell = ws.cell(row=row, column=col)
		timeCell.value = headerText
		timeCell.alignment = wf.centerAlignment
		timeCell.font = Font(size=fontSize, bold=True)
		timeCell.border = wf.outsideBorder


	def createTitle(self, row, col):
		ws = self.__ws
		wf = self.__wf
		dateString = self.__date.strftime('%m/%d/%Y')
		name = 'Name: ' + self.__name
		group = self.__group

		titleCellHeight = wf.titleCellHeight
		titleFontSize = wf.titleFontSize

		title = 'CSSC ' + group

		maxCol = ws.max_column
		maxTitleCol = maxCol*1/3
		maxDateCol = maxCol*2/3

		wf.setMerge(row, row, col, maxTitleCol)
		wf.setMerge(row, row, maxTitleCol + 1, maxDateCol)
		wf.setMerge(row, row, maxDateCol + 1, maxCol)

		ws.cell(row=row, column=col).value = title
		ws.cell(row=row, column=maxTitleCol + 1).value = dateString
		ws.cell(row=row, column=maxDateCol + 1).value = name

		ws.row_dimensions[row].height = titleCellHeight

		ws.cell(row=row, column=col).font = Font(size=titleFontSize, bold=True)
		ws.cell(row=row, column=maxTitleCol + 1).font = Font(size=titleFontSize, bold=True)
		ws.cell(row=row, column=maxDateCol + 1).font = Font(size=titleFontSize, bold=True)

		wf.setCenterAlignment(row, row, col, maxDateCol + 1)


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

def shortenTeacherName(teacherName):
	if teacherName == 'To Be Determined':
		return 'TBD'
	elif teacherName == None:
		return None
	else:
		return teacherName
