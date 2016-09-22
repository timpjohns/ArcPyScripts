#Description: Takes a list of rasters and creates table for each polygon of each raster
# Requirements: Spatial Analyst Extension
# Author: Timothy Johnson
# Date: 11/20/14

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import os
start_time = time.time()

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

# Set environment settings
env.workspace = r"F:\TimData\WB_Dryland_Report\rasterClip"
#Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("GeoStats")

# Get the list of rasters to process
raster_list = arcpy.ListRasters( )
print raster_list

poly_list = arcpy.ListFeatureClasses( )
print poly_list

i=1
for polygon in poly_list:

    for raster in raster_list:

        # Define name and location of output data
        #name = str(raster) + str(polygon) + "_extract.dbf"
        name = str(i)+ "_.dbf"
        # Execute clip
        arcpy.ExtractValuesToTable_ga(polygon, raster, name, "", "")
        i*=10

        print "processing " + raster + "complete..."
    print "processing " + polygon + "complete..."
print time.time() - start_time, "seconds, finished"
