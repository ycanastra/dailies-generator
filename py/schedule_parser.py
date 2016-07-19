from bs4 import BeautifulSoup
import urllib2
import datetime
import re

from schedule_event import ScheduleEvent

class ScheduleParser:
	def __init__(self, soup):
		self.__soup = soup

	def getScheduleEvents(self):
		soup = self.__soup
		events = []

		mydivs = soup.findAll('div', { 'class' : 'calendar_event_weekly' })#, 'title' : labs[i] })

		for item in mydivs:
			blah = item.get_text('|', strip=True).split('|')

			for j in range(len(blah)):
				blah[j] = blah[j].encode('ascii','ignore')

				times = self.__getTimes(blah[-2])
				startTime = times[0]
				endTime = times[1]

			if len(blah) == 3:
				events.append(ScheduleEvent(startTime, endTime, item['title'], blah[0], None))

			else:
				events.append(ScheduleEvent(startTime, endTime, item['title'], blah[0], blah[1]))

		return events

	def __getTimes(self, timeString):
		startStr = timeString.split('-')[0]
		endStr = timeString.split('-')[1]

		startHour = int(re.search(r'\d+', startStr).group())
		endHour = int(re.search(r'\d+', endStr).group())

		startMinute = 0
		endMinute = 0

		if ':' in startStr:
			startMinute = 30
		if ':' in endStr:
			endMinute = 30

		if startStr[-1] == 'p' and startHour != 12:
			startHour += 12
		if endStr[-1] == 'p' and endHour != 12:
			endHour += 12

		startTime = datetime.time(startHour, startMinute)
		endTime = datetime.time(endHour, endMinute)

		return (startTime, endTime)
