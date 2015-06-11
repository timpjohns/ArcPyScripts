'''
Created on Jun 11, 2015

@author: timothyjohnson
'''

# Description: 
# Sums pixels for each year and each country in a table to analyze nighttime light data. Sum pixels after the DN threshold and adjusted for growth

# Requirements: arcGIS license, Spatial Analyst Extension

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

# create list of file locations to save outputs
filelist = [r"F:\TimData\UrbanGravity\Peru\timeseries\mosaic" + "\\",                         
            r"F:\TimData\UrbanGravity\Peru\timeseries\ZonalSumDNmosaic" + "\\", 
            r"F:\TimData\UrbanGravity\China\timeseries\mosaic" + "\\",
            r"F:\TimData\UrbanGravity\China\timeseries\ZonalSumDNmosaic" + "\\",
            r"F:\TimData\UrbanGravity\Mexico\timeseries\mosaic" + "\\",
            r"F:\TimData\UrbanGravity\Mexico\timeseries\ZonalSumDNmosaic" + "\\",
            r"F:\TimData\UrbanGravity\India\timeseries\mosaic" + "\\", 
            r"F:\TimData\UrbanGravity\India\timeseries\ZonalSumDNmosaic" + "\\",
            r"F:\TimData\UrbanGravity\Chile\timeseries\mosaic" + "\\",
            r"F:\TimData\UrbanGravity\Chile\timeseries\ZonalSumDNmosaic" + "\\", 
            r"F:\TimData\UrbanGravity\Uganda\timeseries\mosaic" + "\\", 
            r"F:\TimData\UrbanGravity\Uganda\timeseries\ZonalSumDNmosaic" + "\\",
            r"F:\TimData\UrbanGravity\Uganda\timeseries\mosaic\clip" + "\\",
            r"F:\TimData\UrbanGravity\Kenya\timeseries\mosaic" + "\\", 
            r"F:\TimData\UrbanGravity\Kenya\timeseries\ZonalSumDNmosaic" + "\\",
            r"F:\TimData\UrbanGravity\Kenya\timeseries\mosaic\clip" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\mosaic" + "\\",
            r"F:\TimData\UrbanGravity\Bangladesh\ZonalSumDNmosaic" + "\\"]

#Define function to create folders if they do not already exist
def makefiles():
    for files in filelist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  


#Define clip function to clip rasters whose boundary is not precisely the boundary of the admin shapefile
def cliprasters(shapefile, num1, num2, repname):
    # Set initial workplace of nighttime raster files
    env.workspace = filelist[num1]
    #create raster list to iterate through 
    raslist = arcpy.ListRasters()    
    # clip all rasters to boundary of India
    print raslist
    for ras in raslist:
        # Define name and location of output data
        startname = str(ras)+ "_clip.tif"
        name = startname.replace(repname, "")  
        # Execute set null
        arcpy.Clip_management(ras, "#" , filelist[num2] + name, shapefile, "255", "ClippingGeometry", "MAINTAIN_EXTENT")
        #keep track of rasters completed
        print "Finished clipping file: " + name

#define function to run zonal stats on specified country
def zonalstatscountry(fileloc, countryfile, outname, saveplace):
    # Set initial workplace of nighttime raster files
    env.workspace = filelist[fileloc]
    #create raster list for each year of data
    raslist = arcpy.ListRasters()
    #establish count to keep track of years
    count = 1992
    for ras in raslist:
        name = str(count) + outname
        outZSaT = ZonalStatisticsAsTable(countryfile, "FID", ras, filelist[saveplace] + name, "DATA", "SUM")
        print "Finished creating zonal stats of " + name
        count = count + 1 

# Define function to merge tables together 
def combinetables(file1, table1):
    # Set new workplace where tables are located 
    env.workspace = filelist[file1]
    # list tables in file
    tablelist = arcpy.ListTables()   
    # combine tables so they are all located in shapefile based on common attribute
    for table in tablelist:
        arcpy.JoinField_management (table1, "OID", table, "OID", ["SUM"])
        #keep track of processing
        print "processing " + table + " complete"

# Define how functions are called and used
def main():
    #make folders if they do not exist
    makefiles()  
    #clip rasters
    cliprasters("UgandaBoundary.shp", 10, 12, ".tifUganda_clipped.tif")
    print " \n Finished clipping boundary for Uganda \n"
    cliprasters("KenyaBoundary.shp", 13, 15, ".tifKenya_clipped.tif")
    print " \n Finished clipping boundary for Kenya \n"
    
    #zonal stats and combining output for Peru    
    zonalstatscountry(0, "PeruBoundaryModified.shp", "PeruZonalStats.dbf", 1)
    print " \n Finished processing Zonal Stats for Peru \n"
    combinetables(1, "1992PeruZonalStats.dbf")
    print " \n Finished combining tables for Peru \n"
    
    #zonal stats and combining output for China
    zonalstatscountry(2, "ChinaBoundary_gadmCopy.shp", "ChinaZonalStats.dbf", 3)
    print " \n Finished processing Zonal Stats for China \n"
    combinetables(3, "1992ChinaZonalStats.dbf")
    print " \n Finished combining tables for China \n"
    
    #zonal stats and combining output for Mexico 
    zonalstatscountry(4, "MexicoBoundary.shp", "MexicoZonalStats.dbf", 5)
    print " \n Finished processing Zonal Stats for Mexico \n"
    combinetables(5, "1992MexicoZonalStats.dbf")
    print " \n Finished combining tables for Mexico \n"
    
    #zonal stats and combining output for India
    zonalstatscountry(6, "IndiaGADMBoundary.shp", "IndiaZonalStats.dbf", 7)
    print " \n Finished processing Zonal Stats for India \n"
    combinetables(7, "1992IndiaZonalStats.dbf")
    print " \n Finished combining tables for India \n"
    
    #zonal stats and combining output for Chile
    zonalstatscountry(8, "ChileBoundary.shp", "ChileZonalStats.dbf", 9)
    print " \n Finished processing Zonal Stats for Chile \n"
    combinetables(9, "1992ChileZonalStats.dbf")
    print " \n Finished combining tables for Chile \n"
    
    #zonal stats and combining output for Uganda
    zonalstatscountry(12, "UgandaBoundary.shp", "UgandaZonalStats.dbf", 11)
    print " \n Finished processing Zonal Stats for Uganda \n"
    combinetables(11, "1992UgandaZonalStats.dbf")
    print " \n Finished combining tables for Uganda \n"
    
    #zonal stats and combining output for Kenya
    zonalstatscountry(15, "KenyaBoundary.shp", "KenyaZonalStats.dbf",14)
    print " \n Finished processing Zonal Stats for Kenya \n"
    combinetables(14, "1992KenyaZonalStats.dbf")
    print " \n Finished combining tables for Kenya \n"
    
    #zonal stats and combining output for Bangladesh
    zonalstatscountry(16, "BangladeshAdmin.shp", "BangladeshZonalStats.dbf", 17)
    print " \n Finished processing Zonal Stats for Bangladesh \n"
    combinetables(17, "1992BangladeshZonalStats.dbf")
    print " \n Finished combining tables for Bangladesh \n"

#execute main if code is run
if __name__ == "__main__": 
    main()

#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"