#!/bin/bash
## Script for converting address data to OSM importable address list. 

# Need to open Assess.dbf in libre office calc and save as text csv file first with ':' as delimiter
## !! Also need to make sure no data is missing!

## Usage l3ToOSM.sh <CSV_FILE_FROM_PREVIOUS_STEP> "<STRING_TO_SEARCH>" 

STATE='MA'

## Check for arguments
if [ $# -ne 2 ]; then
	# here we don't have two argments so print usage
	echo -e "Usage: $0 <CSV> <STRING>\n"
	echo -e "Where <CSV> is a colon sparated list of the L3 parcel ESRI shapefile address database"
	echo -e "And <STRING> is a uniq string to search for to remove address nodes in JOSM prior to uploading to OSM\n"
	exit
fi



## Print warnings
echo -e '#########\nPLEASE READ AND ACCEPT!!\n\nThis script assumes the following:'
echo -e '- The MXXXAssess.dbf (XXX=numbers) file with all address data has been opened in libre office and converted to a ":" delimited csv file'
echo -e '- Be sure NOT to upload address nodes, but merge them with buildings and REMOVE THE NOTES!'
echo -e '- Full instructions can be found on my blog post. -xunilOS Or feel free to email me fhunterz@verizon.net\n'

echo 'Do you accept the above? [y/n]'
read accept
if [ $accept != "y" ]; then
	echo 'Please accept by entering "y"'
	exit
fi



# Extract any entries with missing data
python2.7 extractStatePlane.py ${1}


# Covert to lat and long
gdaltransform -s_srs EPSG:2249 -t_srs EPSG:4326 < tmpStatePlane.csv > tmpLatLon.csv

# Reformat lat and lon into lat,lon
cat tmpLatLon.csv | awk -F ' ' '{print $2":"$1":"}' > tmpLatLonFormatted.csv

# Save the lat nd long into a file with address data in below example format
# lat,lon,housnumber,street,city,zip

paste -d '' tmpLatLonFormatted.csv tmpAddressData.csv > tmpL3AddressData.csv

# Remove unnecessary files 
rm -rf tmpAddressData.csv tmpLatLon.csv tmpLatLonFormatted.csv tmpStatePlane.csv

# Run python script to export addresses as nodes

python2.7 csvToOSM.py ${1} ${STATE} ${2}

rm -rf tmpL3AddressData.csv







