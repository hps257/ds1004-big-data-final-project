from __future__ import print_function

import sys
import string
from operator import add
from pyspark import SparkContext
from csv import reader

if __name__ == "__main__":
	sc = SparkContext()

	lines = sc.textFile(sys.argv[1], 1)
	
	lines = lines.mapPartitions(lambda x: reader(x))
	
	def basetype_string(input):
		try:
			if type(input) == str:
				return "STRING"
		except ValueError:
			return type(input)

	def semantictype_parks(value):
		try: 
			name = value.upper()		
			if (len(name) > 3 and type(name) == str):
				return "Parks Description"
			else:
				return "Other"
		except ValueError:	
				return "Other"		


	def validity_parks(x):
		x = x.upper()
		if (x == '' or x == ' '):
			return "NULL"
		elif (len(x) > 3 and type(x) == str):
			return "VALID"
		else:	
			return "INVALID"
			
	header = lines.take(1)

	lines = lines.filter(lambda x: x!=header).map(lambda x: (x[17]))
	
	column18 = lines.map(lambda x: (x, basetype_string(x), semantictype_parks(x), validity_parks(x)))
						
	column18.saveAsTextFile("column18.out")

	sc.stop()