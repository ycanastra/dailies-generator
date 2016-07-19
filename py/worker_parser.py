import operator
import datetime
import os
import json

from collections import defaultdict
from worker_event import WorkerEvent

schedule = []

# def isRoom(room):
# 	if (room == 'OPCO HSSB' or room == 'OPCO LSCF' or
# 		room == 'Consultant SSMS' or room == 'Consultant BSIF' or
# 		room == 'OPCO 1 PHELPS' or room == 'OPCO 2 PHELPS' or
# 		room == 'Consultant HSSB' or room == 'Consultant LSCF' or
# 		room == 'Consultant 1 PHELPS' or room == 'Consultant 2 PHELPS'):
# 		return True
# 	else:
# 		return False

def dayToNum(day):
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
			'Thursday', 'Friday', 'Saturday']

	return days.index(day)

class WorkerParser:

	def __init__(self, path):
		self.__path = path

	def getWorkerEvents(self):
		path = self.__path
		workerEvents = []

		for item in os.listdir(path):
			file = open(path + item)
			data = json.load(file)
			location = data.keys()[0]
			data = data[location]

			for item in data:
				for day, shifts in item.iteritems():
					day = dayToNum(day)

					for shift in shifts:
						name = shift.values()[0]
						startTime = datetime.datetime.strptime(shift.keys()[0], '%H')
						endTime = startTime + datetime.timedelta(hours=1)

						we = WorkerEvent(name, day, startTime, endTime, location)
						workerEvents.append(we)

		workerEvents = self.__simplifyWorkerEvents(workerEvents)

		return workerEvents

	def __simplifyWorkerEvents(self, workerEvents):
		simplifiedWE = []

		workerEvents.sort(key = operator.itemgetter(4, 1, 2))

		currentName = workerEvents[0].getName()
		currentDay = workerEvents[0].getName()
		currentStartHour = workerEvents[0].getStartTime()
		currentEndHour = workerEvents[0].getEndTime()
		currentLocation = workerEvents[0].getLocation()

		for item in workerEvents:

			if (currentName != item.getName() or
				currentDay != item.getDay() or
				currentLocation != item.getLocation()
			):

				event = WorkerEvent(currentName, currentDay, currentStartHour,
								currentEndHour, currentLocation)
				simplifiedWE.append(event)
				currentStartHour = item.getStartTime()
				currentName = item.getName()

			currentDay = item.getDay()
			currentEndHour = item.getEndTime()
			currentLocation = item.getLocation()

		event = WorkerEvent(currentName, currentDay, currentStartHour,
						currentEndHour, currentLocation)
		simplifiedWE.append(event)

		return simplifiedWE
