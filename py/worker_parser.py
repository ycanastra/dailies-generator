import operator
import datetime
import os
import json

from collections import defaultdict, OrderedDict
from worker_event import WorkerEvent

def dayStringToInt(day):
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
			'Thursday', 'Friday', 'Saturday']

	return days.index(day)

class WorkerParser:
	def __init__(self, path):
		self.__path = path

	def getWorkerEvents(self):
		path = self.__path
		workerEvents = []

		file = open(path)
		data = json.load(file, object_pairs_hook=OrderedDict)

		for location in data.keys():
			for day in data[location].keys():
				for hour in data[location][day].keys():
					name = data[location][day][hour]
					dayInt = dayStringToInt(day)
					startTime = datetime.datetime.strptime(hour, '%H')
					endTime = startTime + datetime.timedelta(hours=1)

					we = WorkerEvent(name, dayInt, startTime, endTime, location)
					workerEvents.append(we)

		workerEvents = self.__simplifyWorkerEvents(workerEvents)

		return workerEvents

	# TODO make this better. i'm sure there is a better way to do this
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
