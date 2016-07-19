from lab import Lab

class LabCreator:

	def __init__(self, cardinality):
		self.__labNames = ['BSIF 1217', 'HSSB 1203F OA', 'LSCF 1804 OA', 'LSCF 1805', 'LSCF 1806',
					'Phelps 1513', 'Phelps 1514', 'Phelps 1517', 'Phelps 1518',
					'Phelps 1521 OA', 'Phelps 1525', 'Phelps 1526', 'Phelps 1529',
					'Phelps 1530', 'SSMS 1005', 'SSMS 1007', 'SSMS 1301', 'SSMS 1302',
					'SSMS 1303', 'SSMS 1304'
		]

		self.__labNamesEast = ['BSIF 1217', 'LSCF 1805', 'LSCF 1806',
					'Phelps 1513', 'Phelps 1514', 'Phelps 1517', 'Phelps 1518',
					'Phelps 1525', 'Phelps 1526', 'Phelps 1529', 'Phelps 1530'
		]

		self.__labNamesWest = ['SSMS 1005', 'SSMS 1007', 'SSMS 1301',
							   'SSMS 1302', 'SSMS 1303', 'SSMS 1304'
		]

		self.__cardinality = cardinality

	def createLabs(self):
		cardinality = self.__cardinality
		labs = []

		if cardinality == 'east':
			labNames = self.__labNamesEast
		elif cardinality == 'west':
			labNames = self.__labNamesWest

		for i in range(len(labNames)):
			for j in range(5):
				if j == 4:
					labs.append(Lab(labNames[i], j, 8, 17, 3 + i*2))
				else:
					labs.append(Lab(labNames[i], j, 8, 21, 3 + i*2))

		return labs
