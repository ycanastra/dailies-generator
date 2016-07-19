
class Lab:
	# self.__labName
	# self.__openingTime
	# self.__closingTime

	def __init__(self, labName, day, openingTime, closingTime, colIndex):
		self.__labName = labName
		self.__day = day
		self.__openingTime = openingTime
		self.__closingTime = closingTime
		self.__colIndex = colIndex

	def __str__(self):
		lName = self.__labName
		day = self.__day
		oTime = self.__openingTime
		cTime = self.__closingTime

		return ('LabName: ' + lName + ', Day: ' + str(day) +
				', Time: ' + str(oTime) + ' - ' + str(cTime))

	def __getitem__(self, key):
		if (key == 0):
			return self.__labName
		if (key == 1):
			return self.__day
		if (key == 2):
			return self.__openingTime
		if (key == 3):
			return self.__closingTime

	def getLabName(self):
		return self.__labName

	def getOpeningTime(self):
		return self.__openingTime

	def getClosingTime(self):
		return self.__closingTime

	def getColumnIndex(self):
		return self.__colIndex
