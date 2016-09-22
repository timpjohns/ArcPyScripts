'''
Created on Apr 10, 2015

@author: TIMOTHYJOHNSON
'''
#This script solves an issue with the "Mosaic to New Raster" tool. How do you mosaic one raster of a list with another raster in another list. Turns out
#it is necessary to set the rasters you wish to mosaic as variables, separated by a ";" symbol. Simply writing in list location in tool method does
# not work. Leaving out the ";" symbol also does not seem to work. 

#This script specifically mosaics the current years pixel values with the previous years, taking the maximum value of the overlay. This output, being
#the new "current year", is then mosaiced to the next year using the same methodology. This can be necessary to compute in situations where growth/expansion 
#is being analyzed between years of pixel data.  

# Import system modules
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

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#create list for file locations
filelist = [r"F:\TimData\UrbanGravity\Peru\timeseries\setnull6_raster" + "\\", 
            r"F:\TimData\UrbanGravity\Peru\timeseries\mosaic" + "\\"]

#copy first raster of first date to merge in the output location
arcpy.Copy_management(filelist[0] + "F101992.v4b_web.stable_lights.avg_vis.tif_peruclip.tif_6.tif", filelist[1] +\
                       "F101992.v4b_web.stable_lights.avg_vis.tif_peruclip.tif_6.tif") 
print "copied raster"

# Set new workplace where polygons to merge are located 
env.workspace = filelist[0]

# set count to keep track of place in list during iteration 
mergeindex = 0
county1 = 1

# set name count for merging 
count2 = 1993

#create initial list where mosaiced rasters will go to mosaic to the next raster
mergelist = ["F101992.v4b_web.stable_lights.avg_vis.tif_peruclip.tif_6.tif"]

#create list of all rasters
raslist = arcpy.ListRasters()   

#there are rasters for dates 1992-2013, start count2 at 1993 (which also works as name), stop mosaicing when count2 reaches 2014   
while count2 < 2014:
    #set first raster to mosaic to the first raster in mergelist
    inras1 = filelist[1]+mergelist[mergeindex]
    #set second raster to mosaic as county1 variable, which will be moved to next location in list each iteration
    inras2 = raslist[county1]
    #add input rasters along with ";" separator due to finicky nature of mosaictonewraster 
    finalras = inras1+";"+inras2
    #make sure correct rasters are being mosaiced each iteration
    print finalras
    #set name of output
    name13 = str(count2) + "_mosaic.tif"
    #run mosaic tool
    arcpy.MosaicToNewRaster_management(finalras, filelist[1], name13, '#', '#', '#', "1", "MAXIMUM", '#')
    print "finished merging datasets, created new " + str(count2)
    #append output to first location in mergelist to use in next iteration
    mergelist.insert(0, name13)
    #add 1 to county1 and count2 variables to move location in lists
    county1 = county1 + 1
    count2 = count2 + 1   
    
print "finished mosaicing datasets. It took " + time.time() - start_time + " seconds"