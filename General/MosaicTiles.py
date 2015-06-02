'''
Created on Jun 1, 2015

@author: TIMOTHYJOHNSON
'''
#This script is used for mosaicing the MODIS tiles for each year

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

filelist = [r"F:\TimData\MODISLandCover\2010\subset" + "\\",
            r"F:\TimData\MODISLandCover\2010\subset\mosaic" + "\\",
            r"F:\TimData\MODISLandCover\2011\subset" + "\\",
            r"F:\TimData\MODISLandCover\2011\subset\mosaic" + "\\",
            r"F:\TimData\MODISLandCover\2012\subset" + "\\",
            r"F:\TimData\MODISLandCover\2012\subset\mosaic" + "\\"]

rasnamelist = ["2010_MosaicMODIS.tif", "2011_MosaicMODIS.tif", "2012_MosaicMODIS.tif"]

#Define function to create folders if they do not already exist
def makefiles():
    for files in filelist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  
            
#Define function to copy raster to another file location for future use in mosaic function
def copyraster(file1, file2, inras, outras):
    #copy first raster of first date to merge in the output location
    arcpy.Copy_management(filelist[file1] + inras, filelist[file2] + outras) 
    print "copied raster " + str(outras)

def mosaicrasters(folder1, folder2, rasname):
    # Set initial workplace of hdf files
    env.workspace = filelist[folder1]
    raslist = arcpy.ListRasters()
    for ras in raslist:
        #name = str(date) + "_MODISmosaic.tif"
        #arcpy.MosaicToNewRaster_management(ras, filelist[folder2], name, "#", "#", "#", "1", "LAST","#") 
        arcpy.Mosaic_management(ras, filelist[folder2]+rasnamelist[rasname], "LAST", "#","#","#","#","#","#")
        print "finished processing " + str(ras)

##########main############ 
def main():
    makefiles()
    copyraster(0, 1,"0.hdf2010_subset.tif" , rasnamelist[0])
    mosaicrasters(0,1,0)
    copyraster(2, 3,"315.hdf2011_subset.tif" , rasnamelist[1])
    mosaicrasters(2,3,1)
    copyraster(4, 5,"632.hdf2012_subset.tif" , rasnamelist[2])
    mosaicrasters(4,5,2)
    print "Test Done"
    
#execute main if code is run
if __name__ == "__main__": 
    main() 
 
         
#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"