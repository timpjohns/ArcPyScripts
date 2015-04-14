#Description: Take a list of NetCDF file and creates a raster for each file. Averages daily to monthly
# Author: Timothy Johnson
# Date last modified: 11/18/14

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
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\jan2005"
#Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("GeoStats")

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\jan2005\janRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\jan2005\janRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "jan2005Mosaic", "Jan2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "january finished" "\n"

#######
####february
#######
# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\feb2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\feb2005\febRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\feb2005\febRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "feb2005Mosaic", "feb2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "feb finished" "\n"

#######
####march
#######
# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\mar2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\mar2005\marRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\mar2005\marRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "mar2005Mosaic", "mar2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "march finished" "\n"

#######
####april
#######
# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\apr2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\apr2005\aprRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\apr2005\aprRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "apr2005Mosaic", "apr2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "april finished" "\n"


#######
####may
#######


# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\may2005"


# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\may2005\mayRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\may2005\mayRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "may2005Mosaic", "may2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "may finished""\n"

#######
####june
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\june2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\june2005\juneRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\june2005\juneRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "june2005Mosaic", "june2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "june finished" "\n"

#######
####july
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\july2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\july2005\julyRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\july2005\julyRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "july2005Mosaic", "july2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "july finished" "\n"

#######
####august
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\aug2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\aug2005\augRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\aug2005\augRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "aug2005Mosaic", "aug2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "august finished" "\n"

#######
####september
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\sept2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\sept2005\septRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\sept2005\septRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "sept2005Mosaic", "sept2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print "\n" "september finished" "\n"

#######
####october
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\oct2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\oct2005\octRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\oct2005\octRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "oct2005Mosaic", "oct2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print time.time() - start_time, "seconds, finished"

print "\n" "october finished" "\n"

#######
####november
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\nov2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\nov2005\novRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\nov2005\novRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "nov2005Mosaic", "nov2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print time.time() - start_time, "seconds, finished"

print "\n" "november finished" "\n"

#######
####december
#######

# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\dec2005"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\dec2005\decRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\dec2005\decRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "dec2005Mosaic", "dec2005.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")


print "\n" "december finished" "\n"

#######
####december 2004
#######


# Set environment settings
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\dec2004"

# Get the list of rasters to process
cdf_list = arcpy.ListFiles("*.nc")
print cdf_list

for cdf in cdf_list:
    name = str(cdf) + "_raster.tif"
    newpath = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\dec2004\decRasters"
    name2 = newpath + '/' + name + "_final.tif"
    arcpy.MakeNetCDFRasterLayer_md(cdf,"sm","lon","lat",name)
    arcpy.CopyRaster_management(name,name2)

    print "processing " + cdf + "copy raster complete..."

#set new workspace
env.workspace = r"F:\TimData\AfricanIrrigationStudy\Ethopia\bioIndicat\SoilMoisture\dec2004\decRasters"

#create raster list to mosaic
ras_list = arcpy.ListRasters( )
print ras_list

#execute mosaic 
arcpy.MosaicToNewRaster_management(ras_list, "dec2004Mosaic", "dec2004.tif", "#", "32_BIT_FLOAT", "#", "1", "MEAN","#")

print time.time() - start_time, "seconds, finished"

print "\n" "december 2004 finished" "\n"

print time.time() - start_time, "seconds, finished"
