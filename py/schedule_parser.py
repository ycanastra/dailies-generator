import urllib2
import re

from bs4 import BeautifulSoup
from datetime import datetime

from schedule_event import ScheduleEvent

class ScheduleParser:
	def __init__(self, soup):
		self.__soup = soup

	def getScheduleEvents(self):
		soup = self.__soup
		events = []

		mydivs = soup.findAll('div', { 'class' : 'calendar_event_weekly' })

		for item in mydivs:
			eventArray = item.get_text('|', strip=True).split('|')

			for j in range(len(eventArray)):
				eventArray[j] = eventArray[j].encode('ascii','ignore')

				times = self.__getTimes(eventArray[-2])
				startTime = times[0]
				endTime = times[1]
				lab = item['title']
				eventName = eventArray[0]

			if len(eventArray) == 3: # Has no instrcutor name
				newSE = ScheduleEvent(startTime, endTime, lab, eventName, None)
				events.append(newSE)
			else: # Has a instructor name
				instructorName = eventArray[1]
				newSE = ScheduleEvent(startTime, endTime, lab, eventName, instructorName)
				events.append(newSE)

		return events

	# Takes the timeString and convert it into datetime values
	# Time is in format 9p or 9:30p depending on if it has minutes
	def __getTimes(self, timeString):
		# Adding m at the end so strptime can recognize the am/pm
		startStr = timeString.split('-')[0] + 'm'
		endStr = timeString.split('-')[1] + 'm'

		# If it has a colon it has minutes
		# Otherwise, it doesn't have any minutes
		if ':' in startStr:
			startTime = datetime.strptime(startStr, '%I:%M%p')
		else:
			startTime = datetime.strptime(startStr, '%I%p')
		if ':' in endStr:
			endTime = datetime.strptime(endStr, '%I:%M%p')
		else:
			endTime = datetime.strptime(endStr, '%I%p')

		return (startTime, endTime)
