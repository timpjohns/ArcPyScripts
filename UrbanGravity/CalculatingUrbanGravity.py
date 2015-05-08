'''
Created on May 08, 2015

@author: TIMOTHYJOHNSON
'''

# Description: 
# The goal is to show the growth of nighttime lights from 1992-2013, viewing only the growth, in cities over 50k in population in Bangladesh and 6DN.
# Because methodologies differ in the satellite imagery classification, sometimes areas falsely show a decrease in urban lights from one year to another.
# To correct for this, only areas of growth are considered between years. The extent of urban lights from 1992 for example will be passed to 1993 and 
# only new lights will be viewed. A table showing the area of the extent of pixels (essentially the urban extent) is created. This table also contains 
# the number of brightness pixels per area. The following script involves many steps, all require an arcGIS license.     

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
filelist = [r"F:\TimData\UrbanGravity\Bangladesh" + "\\",
            r"F:\TimData\UrbanGravity\Bangladesh\setnull6_raster" + "\\",
            r"F:\TimData\UrbanGravity\Bangladesh\mosaic" + "\\",
            r"F:\TimData\UrbanGravity\Bangladesh\polygon" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\dissolve" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\UrbanAreaPop" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\SpatialJoin" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\Merge" + "\\",
            r"F:\TimData\UrbanGravity\Bangladesh\erase" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\ZonalStats" + "\\", 
            r"F:\TimData\UrbanGravity\Bangladesh\project" + "\\"]

#Define function to create folders if they do not already exist
def makefiles():
    for files in filelist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  

# Set initial workplace of nighttime raster files
env.workspace = filelist[0]

#define shapefile variable to be used to keep track of table outputs
pnt = "Bangladesh50kPop.shp"

#define raster to copy later
raster1992 = "F101992.v4b_web.stable_lights.avg_vis_6.tif"

#Define function to set null the value of raster less than 6 
def setrastertonull():
    # create list of nighttime light rasters from 1992-2013 so that they can be iterated through
    raslist = arcpy.ListRasters()
    # first set <6 to null in raster list 
    for ras in raslist:
        # Define name and location of output data
        startname = str(ras)+ "_6.tif"
        name = startname.replace("_clip2.tif", "") 
        # Execute set null
        outNull = SetNull(ras, ras, "\"Value\" < 6")
        outNull.save(filelist[1] + name)
        print "processing " + ras + " complete..."

#Define function to copy raster to another file location for future use in mosaic function
def copyraster():
    #copy first raster of first date to merge in the output location
    arcpy.Copy_management(filelist[1] + raster1992, filelist[2] + raster1992) 
    print "copied raster"

#Define function to mosaic previous years raster with current years to get the new added extent. This allows for viewing only the
#growth in both light intensity and extent of the light pixels
def mosaicfunction():
    # Set new workplace where rasters to mosaic are located 
    env.workspace = filelist[1]
    # set count to keep track of place in list during iteration 
    mergeindex = 0
    county = 1
    # set name count for merging 
    count = 1993
    #create initial list where mosaiced rasters will go to mosaic to the next raster
    mergelist = [raster1992]
    #create list of all rasters
    raslist = arcpy.ListRasters()   
    #there are rasters for dates 1992-2013, start count2 at 1993 (which also works as name), stop mosaicing when count2 reaches 2014   
    while count < 2014:
        #set first raster to mosaic to the first raster in mergelist
        inras1 = filelist[2]+mergelist[mergeindex]
        #set second raster to mosaic as county1 variable, which will be moved to next location in list each iteration
        inras2 = raslist[county]
        #add input rasters along with ";" separator due to finicky nature of "mosaic to new raster" tool 
        finalras = inras1+";"+inras2
        #make sure correct rasters are being mosaiced each iteration
        print finalras
        # Define name and location of output data. Start name with Z to make sure they are organized right in files
        name = "Z" + str(count) + "_mosaic.tif"
        #run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras, filelist[2], name, '#', '#', '#', "1", "MAXIMUM", '#')
        print "finished merging datasets, created new " + str(count)
        #append output to first location in mergelist to use in next iteration
        mergelist.insert(0, name)
        #add 1 to county and count variables to move location in lists
        county = county + 1
        count = count + 1      

#Define function to convert raster to polygon, dissolve the multipart polygons into one piece, select polygons that intersect 
#with cities, and do spatial join to get names of cities in polygon 
def rastertopolydissolvejoin():
    # Set new workplace of nighttime raster files that have been mosaiced
    env.workspace = filelist[2]
    #create rasterlist to iterate through
    raslist = arcpy.ListRasters()
    # set count to keep track of output name of files 
    count = 1991
    # For each raster in the raster list do the following
    for ras in raslist:
        # Define count variable to keep track of naming
        count = count + 1
        #print which file is being worked on
        print "\n Processing " + str(count) + " raster \n"
        # Define name and location of output data
        name = str(count) + "_polygon.shp"
    
        # To start, first convert nighttime pixels to polygons so that the extent of connected pixels can be created for the whole country.
        # Execute clip
        arcpy.RasterToPolygon_conversion(ras, filelist[3] + name, "NO_SIMPLIFY", "VALUE")
        #keep track of processing 
        print "\n Processing " + name + " complete. Finished converting " + ras + "to polygon"  

        # dissolve each polygon so that the whole polygon representing the urban area can be selected
        name2 = str(count) + "_dissolved.shp"
        arcpy.Dissolve_management(filelist[3] + name, filelist[4] + name2, "#", "#", "SINGLE_PART", "#")
        #keep track of processing
        print "\n Processing " + name2 + " complete. Finished dissolving " + name
    
        # Before selecting polygons that overlap cities, first make feature layer to use select by location
        namefl = str(count) + "_featurelayer"
        arcpy.MakeFeatureLayer_management(filelist[4] + name2, filelist[4] + namefl)
    
        # select polygons that intersect with cities  
        arcpy.SelectLayerByLocation_management (filelist[4] + namefl, "INTERSECT", filelist[0]+pnt, "#", "NEW_SELECTION")

        # Create layer from selected features
        name3 = str(count) + "_IntersectUrban.shp"
        arcpy.CopyFeatures_management(filelist[4] + namefl, filelist[5] + name3, "#", "#", "#", "#")   
        #keep track of processing
        print " \n Processing " + name3 + " complete. Finished copying selected features from " + namefl
    
        # Spatial Join to get names of cities stored in Att. table
        name4 = str(count) + "_SpatialJoin.shp"
        arcpy.SpatialJoin_analysis(filelist[5] + name3, filelist[0]+pnt, filelist[6] + name4, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT", "#", "#")   
        #keep track of processing
        print "\n Processing " + name4 + " complete. Finished doing spatial join on " + name3

#Define function to copy shapefile to new locations for analysis
def copyshapefile(filenum):
    # #Copy shapefile used for later analysis in the correct folders
    arcpy.Copy_management(filelist[6] + "1992_SpatialJoin.shp", filelist[filenum] + "1992_SpatialJoin.shp") 
    #keep track of processing
    print "copied raster"

# Define function to run Zonal Stats for every polygon to get sum of DNs of Nighttime lights
def zonalstats():
    # Set workplace for spatially joined polygons to generate list
    env.workspace = filelist[6]
    # create list of polygons at this folder location
    polylist = arcpy.ListFeatureClasses()
    # create another file location for raster list
    env.workspace = filelist[2]
    # create another raster list for different location 
    raslist = arcpy.ListRasters()
    # set variable names for keeping track of filename and polylist location 
    count = 1992
    count2 = 0
    for ras in raslist:
        #define output name
        name = str(count) + "_ZonalSum.dbf"
        outZSat = ZonalStatisticsAsTable(filelist[6] + polylist[count2], "SCHNM", ras, filelist[9] + name, "DATA", "SUM")
        #keep track of processing
        print " \n Processing " + str(count) + " complete. Finished doing zonal stats"
        count = count + 1
        count2 = count2 + 1

# Define function to merge tables together and add to table in shapefile
def combinetables():
    # Set new workplace where tables are located 
    env.workspace = filelist[9]
    # list tables in file
    tablelist = arcpy.ListTables()   
    # combine tables so they are all located in shapefile based on common attribute
    for table in tablelist:
        arcpy.JoinField_management (filelist[0] + pnt, "SCHNM", table, "SCHNM", ["SUM"])
        #keep track of processing
        print "processing " + table + " complete"

#Define function to delete unnecessary fields of table
def deletefields():
    # delete unnecessary fields
    arcpy.DeleteField_management(filelist[0] + pnt, ["AREA", "PERIMETER", "P_20000_", "P_20000_ID", "CONTINENT", "UNREGION", "UNSD", "ISO3", "UQID", \
                                                     "TYPE", "POP", "YEAR", "URBORRUR", "POPSRC", "SRCTYP", "LOCNDATSRC", "COORDSRCE", "POLYGONID", "SCALE", "ANGLE"])
    print "fields deleted"

#Define function to calculate the area of each urban extent/polygon. First projects each polygon into a projected coordinate system that meters 
#can be calculated. Then a field in the shapefile is added and the area field is calculated. 
def calculatearea():
    # Set new workplace where merged and dissolved polygons are located
    env.workspace = filelist[6]
    # create list of polygons
    polylist = arcpy.ListFeatureClasses()
    #create count to keep track of files in list
    count = 1992
    for poly in polylist:
        #Change projection to appropriate projection for country
        name = str(count) + "_project.shp"
        arcpy.Project_management(poly, filelist[10] + name, "PROJCS['WGS_1984_Plate_Carree',GEOGCS['GCS_WGS_1984',DATUM\
        ['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION\
        ['Plate_Carree'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]",\
        "", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT\
        ['Degree',0.0174532925199433]]")
        #keep track of processing
        print "Finished processing " + str(count)  
    
        # Add a field called area to each shapefile
        arcpy.AddField_management(filelist[10] + name, "area2", "DOUBLE", "#", "#", "#", "#", "#", "#", "#",) 
        #keep track of processing 
        print "Finished adding area field to table of " + str(count)   
    
        # calculate area in kilometers in the area2 field just created
        arcpy.CalculateField_management(filelist[10] + name, "area2", '!shape.area@kilometers!', "PYTHON_9.3")
        #keep track of processing
        print "Finished calculating area field to table of " + str(count)  
    
        count = count + 1

#Define function to add the area field to the shapefile
def addareafield():  
    # Set new environment settings for projected polygons
    env.workspace = filelist[10]    
    #create list of polygons 
    polylist = arcpy.ListFeatureClasses()
    for poly in polylist:
        arcpy.JoinField_management (filelist[0] + pnt, "SCHNM", poly, "SCHNM", ["AREA2"])
        #keep track of processing
        print "processing " + poly + " complete"    

#####------Main------######

#Call function to make new folders if necessary
makefiles()

#Call function to set null the value of raster less than 6 
setrastertonull()

#Call function to copy raster to another file location for future use in mosaic function
copyraster()

#Call function to mosaic previous years raster with current years to get the new added extent.
mosaicfunction()

#Call function to convert raster to polygon, dissolve the multipart polygons into one piece, select polygons that intersect 
#with cities, and do spatial join to get names of cities in polygon 
rastertopolydissolvejoin()

#Call function to copy shapefile to folder number 7 in folderlist for future analysis
copyshapefile(7)

#Call function to copy shapefile to folder number 8 in folderlist for future analysis
copyshapefile(8)

# Call function to run Zonal Stats for every polygon to get sum of DNs of Nighttime lights
zonalstats()

#Call function to merge tables together and add to table in shapefile
combinetables()

#Call function to delete unnecessary fields of table
deletefields()

#Call function to calculate the area of each urban extent/polygon.
calculatearea()

#Call function to add the area field to the shapefile
addareafield()

#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"