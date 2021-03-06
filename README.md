# L3ParcelToOSM
Scripts to convert MassGIS L3 Parcel data to a JOSM importable OSM file format for mass importing of addresses to Open Street Map 

# Software requirements
This code requires:
* Python2.7 
* gdaltransform (yum install gdal  - on a fedora box)
* Some flavor of Linux with access to the Terminal 

# Install
Simply download the scipts into a directory and follow the below istructions to execute. 
Or view them on my blog on [OpenStreetMaps](https://www.openstreetmap.org/user/xunilOS/diary/35076).

# What each script does
l3ToOSM.sh: This is the master script for executing the conversion and will call the below two scripts. 

extractStatePlane.py: This script extracts the state plane data from the csv file provided to l3ToOSM. It is required to extract the state plane data in order to convert it to lat and long values. It also converts shortened street names (ex. rd to road st to street). If there is any data missing in an entry for the L3 parcel data, it is omitted from the conversion. 

csvToOSM.py: This script will take the collected data from the ESRI L3 Parcel data file and convert it into a JOSM importable file type (.osm xml file)


# Running the scripts (High level Overview)
# High level overview
This section lists the high level overview of the process. For more details see below

* Download the scripts L3ToOSM scripts
* Download MassGIS ESRI shapefile for the town
* Export shapefile database to csv
* Run script to convert to OSM importable file
* Import into JOSM for editing and merge address data with buildings
* Uploading to OSM
* Validation and error checking

# Detailed steps for procedure

## Download the scripts L3ToOSM scripts
Head over to my [github project](https://github.com/linuxuis/L3ParcelToOSM) to download the project and read the README for software dependencies. 

## Download MassGIS ESRI shapefile for the town
* Download L3 parcel data from the [MassGIS website](http://www.mass.gov/anf/research-and-tech/it-serv-and-support/application-serv/office-of-geographic-information-massgis/datalayers/download-level3-parcels.html) - the zip file to download is under the ESRI Shapefiles column named something like L3_SHP_MXXX_<TOWN_NAME>.zip  
* Unzip the file to a temporary location on your computer. 

## Export shapefile database to csv
* With Libre Office Calc (or Microsoft Excel - untested) open the unzipped directory and look for a file named MXXXAssess.dbf (Should be the largest filesize) 
* A popup will ask what character set to use - i selected the first one Western Europe (DOS/OS2-850/International) though you can select Unicode(UTF-8) as well.
* Delete the columns so you are left with state_plane(LOC_ID),Housenumber(Addr_Num),street,city,zipcode
* Click file -> save as 
* Choose a directory to save the csv file (it may be best to use the same directory the scripts are in)
* Make sure to select the Text CSV (.csv) file format
* Click save -> In Libre Office you may get a warning asking if you want to use ODF format, just click "Use text CSV Format"
* IMPORTANT:  In the "Export Text File" box, make sure to change the "Field delimiter" to a colon ":" and click ok to save it.

## Run script to convert to OSM importable file
* Open a terminal and cd into the directory where your script and csv file is saved. 
* run the script with the following arguments: 
l3ToOSM.sh <CSV_FILE_FROM_PREVIOUS_STEP> "<STRING_TO_SEARCH>" 
Where STRING_TO_SEARCH is captured in quotes and is data that will be added to a note for each address to be used for deleting address nodes after they have been merged with buildings. This is to prevent duplication of data and it is better to have address data tagged with a building than floating around as a single node. Make sure this is unique (ex: xunilOSMassAddressUploadDeleteMe)
NOTE: For now this script only works for Massachusetts L3 Parcel data and in the mainland, not the islands like Marthas Vineyard etc.. For more information read about the [State Plane Coordinate System](https://en.wikipedia.org/wiki/State_Plane_Coordinate_System) specifically the state plane zones. 
* The script is very fast and should complete within a second or less. Please note that the street data in the L3 database shortens the names. Ex Road would be RD and Street would be ST. I have added logic into the script to handle this, however it may be possible that I could have missed an abbreviation or two. See the below section on Validation and error checking on how to handle this. 

## Import into JOSM for editing
* The script should have created a new file named MXXXAssess.csv.osm. This file will contain all the address nodes from the L3 parcel database file. 
* Download a section of the town from OSM
* Open JOSM and click File -> Open
* Select the file and click open
* You should now see all the address nodes for the town in question. 
* Click on the address layer and make it the visible layer
* Select the address nodes that correspond to the section of town you downloaded from OSM
* Press CTRL+Shift+M to merge the selection to Layer1 or whatever layer contains the OSM downloaded data. 
* Add the L3 parcel data as a background as this makes it easier to tell what buildings to merge the address nodes with
* Optional: Add a filter to hide any buldings that have addresses associated with them. I use "addr:housenumber"=* building=yes
* Select an address node and press CTRL+C to copy the node
* Select a building to merge the address data with and press CTRL+Shift+V to merge the two
* Repeat the last two steps until done for the day and ready to upload
* I occasionally check the address data to make sure it is in line with the L3 parcel background data and street names as good habbit. 

## Uploading to OSM
* Prior to uploading to OSM it is very important to remove the address nodes to prevent them  from being duplicated on the map
* IMPORTANT: If you created a filter to hide building with addresses, temporarily deactivate it
* Click edit -> search 
* In the search field look for type:node note="xunilOS ImportAddrPleaseDeleteMe" Where note="" is what you eneterd in the STRING_TO_SEARCH argument. 
* Verify only the address nodes are selected and press delete. 
* Click edit -> search again to remove the note field that was also merged with all the buildings you added address data to. 
* In the searchfield enter note="xunilOS ImportAddrPleaseDeleteMe" Where note="" is what you eneterd in the STRING_TO_SEARCH argument. 
*  In the properties window on the right select the note property and delete all the notes containing the STRING_TO_SEARCH argument. 
* Finally upload the addresses and resolve any errors that the validator may find. 

## Validation and error checking
After uploading to OSM, it is important to review your work to see if address data could be incorrect in case it was not caught prior to uploading to OSM. Ex a street name was not found etc.. The OSM inspector website is a great tool for such a task.
 
* Go to [OSMInspector](http://tools.geofabrik.de/osmi/) and click addresses under the view dropdown. 
* Zoom to the town you were working on and resolve any errors that can be found. 
Typically this may include a misspelled street name etc.. 
