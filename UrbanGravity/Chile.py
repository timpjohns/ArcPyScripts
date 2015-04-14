'''
Created on Apr 8, 2015

@author: TIMOTHYJOHNSON
'''

# Description: 
# The goal is to show the growth of nighttime lights from 1992-2013 in Chile, viewing only the growth, in cities over 100k in population.
# Because methodologies differ in the satellite imagery classification, sometimes areas falsely show a decrease in urban lights from one year to another.
# To correct for this, only areas of growth are considered between years. The extent of urban lights from 1992 for example will be passed to 1993 and 
# only new lights will be viewed. A table showing the area of the extent of pixels (essentially the urban extent) is created. This table also contains the number of 
# brightness pixels per area. The following script involves many steps, all require an arcGIS license.     

# Requirements: arcGIS license, Spatial Analyst Extension

# Import system modules
from __future__ import division
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import os

# start time to calculate time script takes to run
start_time = time.time()

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True


# Set initial workplace of nighttime raster files
env.workspace = r"F:\TimData\UrbanGravity\Chile\timeseries"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# create list of file locations to save outputs
filelist = [r"F:\TimData\UrbanGravity\Chile\timeseries\polygon" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\dissolve" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\UrbanAreaPop" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\SpatialJoin" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\Merge" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\ZonalStats" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\project" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\erase" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries" + "\\", 
            r"F:\TimData\UrbanGravity\Chile\timeseries\dissolve2" + "\\",
            r"F:\TimData\UrbanGravity\Chile\timeseries\setnull8_raster" + "\\"]

#create folders if they do not already exist
for files in filelist:
    if not os.path.exists(files): 
        os.makedirs(files)
        print "made " + files  

# create list of nighttime light rasters from 1992-2013 so that they can be iterated through 
ras_list = arcpy.ListRasters()

# define shapefile variable to be used to keep track of table outputs
pnt = "Chile_100kpop.shp"
#india = "Boundary.shp"

# first set <8 to null in raster list 
for ras in ras_list:
    # Define name and location of output data
    name10 = str(ras) + "_8.tif" 
    # Execute set null
    outNull = SetNull(ras, ras, "\"Value\" < 8")
    outNull.save(filelist[10] + name10)

    print "processing " + ras + "complete..."
    
# Set new workplace of nighttime raster files that have zero values set to null
env.workspace = filelist[10]

ras_listy2 = arcpy.ListRasters()    

'''
# clip all rasters to boundary of India
for rasy2 in ras_listy2:
    # Define name and location of output data
    name11 = str(rasy2) + "_clip.tif" 
    # Execute set null
    arcpy.Clip_management(rasy2, "#" , filelist[11] + name11, filelist[8] + india, "#", "ClippingGeometry", "MAINTAIN_EXTENT")

    print "processing " + rasy2 + "completed clip"
'''
# Set new workplace of nighttime raster files that have zero values set to null
env.workspace = filelist[10]

ras_listy = arcpy.ListRasters()


# set count to keep track of output name of files 
count = 1991

# For each raster in the raster list do the following
for rasy in ras_listy:
    # Define name and location of output data
    count = int(count)
    count = count + 1
    count = str(count)
    print "\n Processing " + count + " raster \n"
    name = count + "_polygon.shp"
    
    # To start, first convert nighttime pixels to polygons so that the extent of connected pixels can be created for the whole country.
    # Execute clip
    arcpy.RasterToPolygon_conversion(rasy, filelist[0] + name, "NO_SIMPLIFY", "VALUE")
    
    print "\n Processing " + name + " complete. Finished converting " + ras + "to polygon"  

    # dissolve each polygon so that the whole polygon representing the urban area can be selected
    name2 = count + "_dissolved.shp"
    arcpy.Dissolve_management(filelist[0] + name, filelist[1] + name2, "#", "#", "SINGLE_PART", "#")

    print "\n Processing " + name2 + " complete. Finished dissolving " + name
    
    # Before selecting polygons that overlap cities, first make feature layer to use select by location
    namefl = count + "_featurelayer"
    arcpy.MakeFeatureLayer_management(filelist[1] + name2, filelist[1] + namefl)
    
    # select polygons that intersect with cities  
    arcpy.SelectLayerByLocation_management (filelist[1] + namefl, "INTERSECT", filelist[8]+pnt, "#", "NEW_SELECTION")

    # Create layer from selected features
    name3 = count + "_IntersectUrban.shp"
    arcpy.CopyFeatures_management(filelist[1] + namefl, filelist[2] + name3, "#", "#", "#", "#")   
    
    print " \n Processing " + name3 + " complete. Finished copying selected features from " + namefl
    
    # Spatial Join to get names of cities stored in Att. table
    name4 = count + "_SpatialJoin.shp"
    arcpy.SpatialJoin_analysis(filelist[2] + name3, filelist[8]+pnt, filelist[3] + name4, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT", "#", "#")   
    
    print "\n Processing " + name4 + " complete. Finished doing spatial join on " + name3


# #Copy shapefile used for later analysis in the correct folders
arcpy.Copy_management(filelist[3] + "1992_SpatialJoin.shp", filelist[4] + "1992_SpatialJoin.shp") 
print "copied raster"

arcpy.Copy_management(filelist[3] + "1992_SpatialJoin.shp", filelist[7] + "1992_SpatialJoin.shp") 
print "copied raster again"

# #Only urban areas that are new between each date should be calculated in sum. To achieve this, the polygon from the previous year is merged to the 
# polygon of the present year. Next, the polygon from the previous year is erased from the polygon of the next year. This leaves just the area of new extent. 
# This area is then used on zonal statistics to get the sum of the new area which is added to the original sum of 1992 to get the sum of each date. 

# Set new workplace where polygons to merge are located 
env.workspace = filelist[3]

# set count to keep track of merging 
count1 = 1

# set second name count for merging 
count2 = 1993

mergelist = ["1992_SpatialJoin.shp"]

polylist = arcpy.ListFeatureClasses()

while count2 < 2014:
    name5 = str(count2) + "_newmerge.shp"
    arcpy.Merge_management([filelist[4] + mergelist[0], polylist[count1]], filelist[4] + name5)
    print "finished merging datasets, created new " + str(count2)
    mergelist.insert(0, name5)
    print "new mergelist: " + str(mergelist)
    count1 = count1 + 1
    count2 = count2 + 1

# Now time to erase the previous years polygon from the current years to get new area. First must dissolve polygon again
# Set new workplace where polygons to merge are located 
env.workspace = filelist[4]

# create list of newly merged polygons
poly_list = arcpy.ListFeatureClasses()

# Set variables for iterating through list 
list1 = 1
list2 = 0
count3 = 1993
count4 = 1992

'''
for poly in poly_list:
    # dissolve polygon 
    name6 = str(count4) + "_dissolved2.shp"
    arcpy.Dissolve_management(poly, filelist[9]+name6, "#", "#", "SINGLE_PART", "#")
    print "Dissolved " + str(name6) + " complete" 
'''    
    # erase polygon
while count3 < 2014:
    name7 = str(count3) + "_erase.shp"
    arcpy.Erase_analysis(poly_list[list1], poly_list[list2], filelist[7] + name7)       
    print "Erased " + str(count3) + " complete"    

    count3 = count3 + 1
    count4 = count4 + 1
    list1 = list1 + 1
    list2 = list2 + 1

# Run Zonal Stats for every polygon to get sum of DNs of Nighttime lights

# Set workplace for erased polygons to generate list
env.workspace = filelist[7]

# create list of polygons
polylist2 = arcpy.ListFeatureClasses()

# create another raster list for different location 
ras_list2 = arcpy.ListRasters()

# Set new workplace where rasters are located to sum values of raster
env.workspace = filelist[10]

# create another raster list for different location 
ras_list2 = arcpy.ListRasters()

# set variable name
count5 = 1992
count101 = 0

for ras2 in ras_list2:
    name8 = str(count5) + "_ZonalSum.dbf"
    outZSat = ZonalStatisticsAsTable(filelist[7] + polylist2[count101], "SCHNM", ras2, filelist[5] + name8, "DATA", "SUM")
    print " \n Processing " + str(count5) + " complete. Finished doing zonal stats"
    count5 = count5 + 1
    count101 = count101 + 1

# Now time to merge tables together and add to table in shapefile

# Set new workplace where tables are located 
env.workspace = filelist[5]

# list tables in file
tablelist = arcpy.ListTables()   

# combine tables so they are all located in shapefile based on common attribute
for table in tablelist:
    arcpy.JoinField_management (filelist[8] + pnt, "SCHNM", table, "SCHNM", ["SUM"])
    print "processing" + table + "complete"


# delete unnecessary fields
arcpy.DeleteField_management(filelist[8] + pnt, ["AREA", "PERIMETER", "P_20000_", "P_20000_ID", "CONTINENT", "UNREGION", "UNSD", "ISO3", "UQID", \
"TYPE", "POP", "YEAR", "URBORRUR", "POPSRC", "SRCTYP", "LOCNDATSRC", "COORDSRCE", "POLYGONID", "SCALE", "ANGLE"])
print "fields deleted"

###########
# #Now time to calculate the area of each urban extent/polygon

# Set new workplace where merged and dissolved polygons are located
env.workspace = filelist[7]

# create list of polygons
polylist3 = arcpy.ListFeatureClasses()

count8 = 1992

for poly3 in polylist3:
    
    # Process: Project. Change projection to appropriate projection for country
    name9 = str(count8) + "_project.shp"
    arcpy.Project_management(poly3, filelist[6] + name9, "PROJCS['WGS_1984_Plate_Carree',GEOGCS['GCS_WGS_1984',DATUM\
    ['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION\
    ['Plate_Carree'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]",\
    "", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT\
    ['Degree',0.0174532925199433]]")

    print "Finished processing " + str(count8)  
    
    # Add a field called area to each shapefile
    arcpy.AddField_management(filelist[6] + name9, "area2", "DOUBLE", "#", "#", "#", "#", "#", "#", "#",)  
    print "Finished adding area field to table of " + str(count8)   
    
    # calculate area in kilometers in the area2 field just created
    arcpy.CalculateField_management(filelist[6] + name9, "area2", '!shape.area@kilometers!', "PYTHON_9.3")
    print "Finished calculating area field to table of " + str(count8)  
    
    count8 = count8 + 1

# #Now, lastly, time to add the area field to the shapefile as well    
# Set new environment settings for projected polygons
env.workspace = filelist[6]    

polylist4 = arcpy.ListFeatureClasses()

for poly4 in polylist4:
    arcpy.JoinField_management (filelist[8] + pnt, "SCHNM", poly4, "SCHNM", ["AREA2"])
    print "processing" + poly4 + "complete"    


print (time.time() - start_time) / 60, "minutes, finished. You freaking did it, you created over 300 files necessary to create the desired output table!"