#!/bin/python1.7

## this script is used to extract the state plane data and store it into a new file
import csv
import sys

# Define number of feet in meter
oneMInFt=3.280839895
DEBUG=False


## Expected input: filenameOfCSV with : delimitation 
## File format: state_plane,Addr_num,street,city,zipcode

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
			if tmp[0] == '' or tmp[1] == '' or tmp[2] == '' or tmp[3] == '' or tmp[4] == '':
				pass
			else:
				# if data is present, save it to new file as AddrNum,streetName,city,zip
				# Extract the street and change rd to road etc 
				rdBEG=tmp[2].rsplit(' ',1)[0].title()			
				rdEND=tmp[2].rsplit(' ',1)[1].title().replace('Ave', 'AVENUE').replace('Av','AVENUE').replace('Cir','CIRCLE').replace('Cmn','COMMON').replace('Cor','CORNER').replace('Ct','COURT').replace('Dr','DRIVE').replace('Ext','EXTENSION').replace('Hts','HEIGHTS').replace('Ln','LANE').replace('Pl','PLACE').replace('St','STREET').replace('Rd','ROAD').replace('Rdg','RIDGE').replace('Sq','SQUARE').replace('Ter','TERRACE').replace('Tpke','TURNPIKE').replace('Trl','TRAIL').replace('Xing','CROSSING').title()
				outAddr.write(tmp[1]+':'+rdBEG+' '+rdEND+':'+tmp[3].title()+':'+tmp[4]+'\n')
				if DEBUG:
					print (tmp[0]+':'+rdBEG+' '+rdEND+':'+tmp[3].title()+':'+tmp[4]+'\n')
				# Save state plane in other file for conversion, but check if in ft or meters, if meters, change to ft			
				if tmp[0][:1] =='M':
					statePlaneFt=str(int(int(tmp[0].split('_')[1])*oneMInFt)) + " " + str(int(int(tmp[0].split('_')[2])*oneMInFt))
				else: 
					statePlaneFt=tmp[0][2:].replace('_',' ')
				outStatePlane.write(statePlaneFt+'\n')
				if DEBUG:
					print(statePlaneFt+'\n')
				
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

