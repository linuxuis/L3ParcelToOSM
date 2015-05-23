#!/bin/python

import sys
import csv

# this script is used to convert addresses to a JOSM importable file of nodes

# get the inputed filename of CSV with addresses
addrCSV=str(sys.argv[1])
state=str(sys.argv[2])
searchString=str(sys.argv[3])

# open file for saving 
try:
	osmOut=open(addrCSV+".osm",'w')
except Exception:
	print("ERROR: Unable to open " + addrCSV+".osm")
	sys.exit()

# Write the XML Headers
osmOut.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' upload='false' generator='JOSM'>\n")

# Open address CSV file to parse and add nodes to OSM file with
try:
	L3Parcel=open(addrCSV,'r')
except Exception:
	print("ERROR: Unable to open "+addrCSV + " in csvToOSM.py")
	osmOut.close()
	sys.exit()

# Iterate through address data and add nodes to osm file
csvReader= csv.reader(L3Parcel,delimiter=':',quotechar='"')
# number for node ids
i=-22222

while True:
	try:
		# read next line Format: lat,lon,houseNum,Street,City,zip
		tmp=next(csvReader)
		# Add the node id and position
		osmOut.write("\t<node id='"+str(i)+"' action='modify' visible='true' lat='"+tmp[0]+"' lon='"+tmp[1]+"'>\n")
		# Add the city
		osmOut.write("\t\t<tag k='addr:city' v='"+tmp[4]+"' />\n")
		# Add the country
		osmOut.write("\t\t<tag k='addr:country' v='US' />\n")
		# Add the housenumber
		osmOut.write("\t\t<tag k='addr:housenumber' v='"+tmp[2]+"' />\n")
		# Add the zipcode
		osmOut.write("\t\t<tag k='addr:postcode' v='"+tmp[5]+"' />\n")
		# Add the State
		osmOut.write("\t\t<tag k='addr:state' v='"+state+"' />\n")
		# Add the street
		osmOut.write("\t\t<tag k='addr:street' v='"+tmp[3]+"' />\n")
		# Add field in note to search on 
		osmOut.write("\t\t<tag k='note' v='"+searchString+"' />\n")
		# End the node
		osmOut.write("\t</node>\n")

		i=i-1
	except StopIteration:
		break


# Write the XML closing tags
osmOut.write("</osm>")


# Close the files
osmOut.close()
L3Parcel.close()

print("Complete! Please import " + addrCSV+".osm" + " into JOSM for address imports")
