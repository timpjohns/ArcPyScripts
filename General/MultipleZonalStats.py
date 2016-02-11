'''
Created on Jul 17, 2015

@author: timothyjohnson

'''

#multiple zonal stats on different rasters for the same districts for Xinshen in Ghana


# Import system modules
from __future__ import division
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import os

# start time to keep track of time script takes to run
start_time = time.time()

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

filelist = [r"F:\TimData\MapsForLiang\GhanaRoads\Ghana.gdb" + "\\",
            r"F:\TimData\MapsForLiang\GhanaRoads\ZonalOutput" + "\\"]

#Define function to create folders if they do not already exist
def makefiles():
    for files in filelist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  

def zonalstats():
    # Set initial workplace of files
    env.workspace = filelist[0]
    #create list of rasters
    raslist = arcpy.ListRasters()
    for ras in raslist:
        name = str(ras) + ".dbf"
        outZSaT = ZonalStatisticsAsTable("District137", "NAME_2", ras, name, "DATA", "SUM")
        print "Finished doing zonal stats for : " + name
   
##########main############ 
def main():
    makefiles()
    zonalstats()
    
#execute main if code is run
if __name__ == "__main__": 
    main() 
   
#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished" 