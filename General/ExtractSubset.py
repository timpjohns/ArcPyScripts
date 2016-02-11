'''
Created on May 29, 2015

@author: TIMOTHYJOHNSON
'''

#This script is used for extracting the hdf file of interest from each tile

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

filelist = [r"F:\TimData\MODISLandCover\2010" + "\\",
            r"F:\TimData\MODISLandCover\2010\subset" + "\\"]

def subsetrasters():
    # Set initial workplace of hdf files
    env.workspace = filelist[0]
    raslist = arcpy.ListRasters()
    for ras in raslist:
        name = str(ras)+ "2010_subset.tif"
        arcpy.ExtractSubDataset_management(ras, filelist[1]+name, "1")
        print "finished processing " + str(name)

##########main############ 
def main():
    subsetrasters()
    
#execute main if code is run
if __name__ == "__main__": 
    main() 
 
         
#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"