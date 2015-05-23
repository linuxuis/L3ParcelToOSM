#!/bin/python1.7

## this script is used to extract the state plane data and store it into a new file
import csv
import sys

## Expected input: filenameOfCSV 


# open a file to place the results of statePlane
try:
	outStatePlane=open('tmpStatePlane.csv','w')
except Exception:
	print("ERROR: Unable to open tmpStatePlane.csv")
	sys.exit()

# open file to place other necessary data
try:
	outAddr=open('tmpAddressData.csv','w')
except Exception:
	print("ERROR: Unable to open tmpAddressData.csv")
	sys.exit()


# Open file for reading
csvFileInput=str(sys.argv[1])
try:
	csvFile= open(csvFileInput,'r')
	csvReader= csv.reader(csvFile,delimiter=':',quotechar='"')
	# We don't care about the first row since it is definitional so throw it out
	tmp = next(csvReader)
	while True:
		try:
			# read next line 
			tmp=next(csvReader)
			# Check if any necessary data is missing and if so, do nothing with line
			if tmp[1] == '' or tmp[12] == '' or tmp[13] == '' or tmp[15] == '' or tmp[16] == '':
				pass
			else:
				# if data is present, save it to new file as AddrNum,streetName,city,zip
				# Extract the street and change rd to road etc 
				rdBEG=tmp[13].rsplit(' ',1)[0].title()			
				rdEND=tmp[13].rsplit(' ',1)[1].title().replace('Ave', 'AVENUE').replace('Av','AVENUE').replace('Cir','CIRCLE').replace('Cmn','COMMON').replace('Cor','CORNER').replace('Ct','COURT').replace('Dr','DRIVE').replace('Ext','EXTENSION').replace('Hts','HEIGHTS').replace('Ln','LANE').replace('Pl','PLACE').replace('St','STREET').replace('Rd','ROAD').replace('Rdg','RIDGE').replace('Sq','SQUARE').replace('Ter','TERRACE').replace('Tpke','TURNPIKE').replace('Trl','TRAIL').replace('Xing','CROSSING').title()
				outAddr.write(tmp[12]+':'+rdBEG+' '+rdEND+':'+tmp[15].title()+':'+tmp[16]+'\n')
				# Save state plane in other file for conversion				
				outStatePlane.write(tmp[1][2:].replace('_',' ')+'\n')
		except StopIteration:
			break

		

except Exception:
	print("ERROR: Unable to open file " + csvFileInput)
	outStatePlane.close()
	outAddr.close()
	sys.exit()


# close files
outStatePlane.close()
outAddr.close()
csvFile.close

