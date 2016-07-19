
class ScheduleEvent:
	def __init__(self, sTime, eTime, location, eName, eTeacher):
		self.__startTime = sTime
		self.__endTime = eTime
		self.__location = location
		self.__eventName = eName
		self.__eventTeacher = eTeacher

	def __str__(self):
		retStr = ('Location: ' + self.__location + ', Time: ' +
				  self.getTimeString() + ', EventName: ' + self.__eventName)

		if self.__eventTeacher:
			retStr += ', EventTeacher: ' + self.__eventTeacher

		return retStr

	def getStartTime(self):
		return self.__startTime

	def getEndTime(self):
		return self.__endTime

	def getLocation(self):
		return self.__location

	def getEventName(self):
		return self.__eventName

	def getEventTeacher(self):
		return self.__eventTeacher

	def getTimeString(self):
		startTime = self.__startTime
		endTime = self.__endTime

		if startTime.minute == 30:
			startStr = startTime.strftime("%I:%M%p")
		else:
			startStr = startTime.strftime("%I%p")
		if endTime.minute == 30:
			endStr = endTime.strftime("%I:%M%p")
		else:
			endStr = endTime.strftime("%I%p")

		startStr = startStr[:-1].lower().lstrip('0')
		endStr = endStr[:-1].lower().lstrip('0')

		return startStr + ' - ' + endStr
