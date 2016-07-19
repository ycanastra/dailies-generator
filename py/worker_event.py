
class WorkerEvent:

	def __init__(self, name, day, startTime, endTime, location):
		self.__name = name
		self.__day = day
		self.__startTime = startTime
		self.__endTime = endTime
		self.__location = location

	def __str__(self):
		retStr = ('Location: ' + self.__location + ', Day: ' + str(self.__day) +
				  ', Name: ' + self.__name + ', Time: ' + str(self.__startTime) +
				  ' - ' + str(self.__endTime))

		return retStr

	def __getitem__(self, key):
		if (key == 0):
			return self.__name
		if (key == 1):
			return self.__day
		if (key == 2):
			return self.__startTime
		if (key == 3):
			return self.__endTime
		if (key == 4):
			return self.__location

	def getName(self):
		return self.__name

	def getDay(self):
		return self.__day

	def getStartTime(self):
		return self.__startTime

	def getEndTime(self):
		return self.__endTime

	def getLocation(self):
		return self.__location

	def getTimeString(self):
		startTime = self.__startTime
		endTime = self.__endTime

		startStr = startTime.strftime('%I%p')
		endStr = endTime.strftime('%I%p')

		startStr = startStr[:-1].lower().lstrip('0')
		endStr = endStr[:-1].lower().lstrip('0')

		return startStr + ' - ' + endStr
