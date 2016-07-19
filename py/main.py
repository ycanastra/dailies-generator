#!/usr/bin/env python

import sys
import datetime
import urllib2
from bs4 import BeautifulSoup

from schedule_parser import ScheduleParser
from worker_parser import WorkerParser
from lab_creator import LabCreator
from workbook_creator import WorkbookCreator

import os


import json


def main():


	employeeShiftsPath = './data/employee_shifts/'
	employeeGroupsPath = './data/employee_groups.json'
	labGroupsPath = './data/lab_groups.json'

	if len(sys.argv) != 4:
		sys.exit('Need 3 arguments')

	name = sys.argv[1]
	group = sys.argv[2]
	date = sys.argv[3]

	dateSplit = date.split('/')
	dateTime = datetime.datetime(int(dateSplit[2]), int(dateSplit[0]), int(dateSplit[1]), 7, 0)

	seconds = (dateTime - datetime.datetime(1970, 1, 1)).total_seconds()
	url = 'http://labschedule.collaborate.ucsb.edu/?ts=' + str(int(seconds))

	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')

	scheduleParser = ScheduleParser(soup)
	scheduleEvents = scheduleParser.getScheduleEvents()

	workerParser = WorkerParser(employeeShiftsPath)
	workerEvents = workerParser.getWorkerEvents()

	# labCreator = LabCreator(group)
	# labs = labCreator.createLabs()

	wbCreator = WorkbookCreator(soup, name, group, dateTime, scheduleEvents,
								workerEvents)
	wbCreator.generateWorkbook()

if __name__ == '__main__':
	main()
