'''
Created on Jul 8, 2015

@author: TIMOTHYJOHNSON
'''
#This script is used for getting the landcover counts per admin area of MODIS landcover data from 2001-2012. 
#For each year, first the rasters are reclassified into one landcover type, where the other landcover types are "NODATA" value, and the landcover
#of interest has a value of 1. Then using the GADM global admin shapefile's FID column, the cells are summed using zonal stats. The final output 
#is a table of each year and each landcover type and how many cells fall into each admin unit. Then the tables are merged, resulting in 7 tables, 
#for the 7 landcover types for each year and the admin they are located in. Then it is simply a matter of naming the landcover types in the tables and 
#joining them together, and creating percentages of landcover for each LC type and admin units of interest. Voila, MODIS land cover changes from 2001-2012
#at the 2nd-5th admin level (depending on country).  

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

#Create list of folder locations
filelist = [r"F:\TimData\MODISLandCover" + "\\",
            r"F:\TimData\MODISLandCover\reclassed" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\water" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\forest" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\shrub" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\grass" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\crop" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\urban" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ReclassedLC\barren" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\water" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\forest" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\shrub" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\grass" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\crop" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\urban" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats\barren" + "\\",
            r"F:\TimData\MODISLandCover\CountryLC\ZonalStats" + "\\"]

#Define function to create folders if they do not already exist
def makefiles():
    for files in filelist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  

#Define function to reclass each raster into just one landcover. Starting with a raster of 1-7 values, individual landcovers are selected to recode
#to one and summarize in zonal stats individually for clarity. LCname is passed as the landcover that will be appended to the end of the file name. 
#Reclassvalues are the values that will be reclassed, depending on the landcover of interest. Filenum is the folder location of the output. 
def reclass(LCname, reclassvalues, filenum):
    # Set initial workplace of hdf files
    env.workspace = filelist[1]
    raslist = arcpy.ListRasters()
    for ras in raslist:
        name = str(ras)+ LCname
        arcpy.gp.Reclassify_sa(ras,"VALUE", reclassvalues, filelist[filenum]+name, "NODATA")
        print "Finished reclassifying: " + name

#define function to perform zonal stats on each of the years 2001-2012 for each land cover, based on the FID global Admin column.
#Function passes: filenum, which is number in filelist to set workplace where rasters are; filename, the name of the file to save in addition to its year;
#and filelistnum, the folder to save the ouput    
def zonalstats(filenum, filename, filelistnum): 
    # Set initial workplace of raster files
    env.workspace = filelist[filenum]
    #create list of rasters in folder location
    raslist = arcpy.ListRasters()
    #establish date of raster to use in name output
    date = 2001
    for ras in raslist:
        #establish name of output, date, plus landcover type of rasters
        name = str(date)+ filename
        #execute zonal stats, using global admin file in folder 0 of filelist, and the FID column as zone. Make sure "Data" is included, otherwise
        #if NODATA zones with even one nodata cell will be ignored. The statistic SUM was chosen, although it should be the same thing as count 
        #which is the main interest
        outZSaT = ZonalStatisticsAsTable(filelist[0]+"GADM.shp", "FID", ras, filelist[filelistnum]+name, "DATA", "SUM")
        #keep track of progress
        print "Finished doing zonal stats on: " + name
        #add one to date
        date = date + 1

# Define function to merge tables together
def combinetables(filelistnum, firsttable):
    # Set new workplace where tables are located 
    env.workspace = filelist[filelistnum]
    # list tables in file
    tablelist = arcpy.ListTables()   
    # combine tables so they are all located in same table based on common attribute
    for table in tablelist:
        arcpy.JoinField_management (firsttable, "FID_", table, "FID_")
        #keep track of processing
        print "processing " + table + " complete"

##########main############ 
def main():
    makefiles()
    reclass("_water.tif", "1 1;2 NODATA;3 NODATA;4 NODATA;5 NODATA;6 NODATA;7 NODATA",2)
    zonalstats(2, "_water.dbf", 9)
    combinetables(9, "2001_water.dbf")
    print "finishing processing data for water"
    reclass("_forest.tif", "1 NODATA;2 1;3 NODATA;4 NODATA;5 NODATA;6 NODATA;7 NODATA",3)
    zonalstats(3, "_forest.dbf", 10)
    combinetables(10, "2001_forest.dbf")
    print "finishing processing data for forest"
    reclass("_shrub.tif", "1 NODATA;2 NODATA;3 1;4 NODATA;5 NODATA;6 NODATA;7 NODATA",4)
    zonalstats(4, "_shrub.dbf", 11)
    combinetables(11, "2001_shrub.dbf")
    print "finishing processing data for shrub"
    reclass("_grass.tif", "1 NODATA;2 NODATA;3 NODATA;4 1;5 NODATA;6 NODATA;7 NODATA",5)
    zonalstats(5, "_grass.dbf", 12)
    combinetables(12, "2001_grass.dbf")
    print "finishing processing data for grass"
    reclass("_crop.tif", "1 NODATA;2 NODATA;3 NODATA;4 NODATA;5 1;6 NODATA;7 NODATA",6)
    zonalstats(6, "_crop.dbf", 13)
    combinetables(13, "2001_crop.dbf")
    print "finishing processing data for crop"
    reclass("_urban.tif", "1 NODATA;2 NODATA;3 NODATA;4 NODATA;5 NODATA;6 1;7 NODATA",7)
    zonalstats(7, "_urban.dbf", 14)
    combinetables(14, "2001_urban.dbf")
    print "finishing processing data for urban"
    reclass("_barren.tif", "1 NODATA;2 NODATA;3 NODATA;4 NODATA;5 NODATA;6 NODATA;7 1",8)
    zonalstats(8, "_barren.dbf", 15)
    combinetables(15, "2001_barren.dbf")
    print "finishing processing data for barren"
    
#execute main if code is run
if __name__ == "__main__": 
    main() 
   
#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished" 

