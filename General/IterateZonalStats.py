'''
Created on Feb 2, 2016

@author: TIMOTHYJOHNSON

Iterates through the CRU data and gets zonal stats for specified admin area. 
Since CRU data is 60km and if an admin area is smaller than a 60km cell it is
given a nodata value in zonal stats, the raster data is first resampled. To 
speed up the process, a buffer around the total admin area is made (to make 
sure all cells are included), and each raster is clipped to the buffer before 
resampling to ~1km2. Then zonal stats are done for each raster. Finally, the 
tables are appended to 5 copies of the shapefile dbf. 5 copies are need since 
there are 1200 rasters, and a dbf table can only hold 255 columns.   
'''
# Import system modules
from __future__ import division
import arcpy
from arcpy import env
from arcpy.sa import *
import os, time


# start time to keep track of time 
start_time = time.time()

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# specify full path location of rasters and admin shapefile first, 
# then specify output of clip folder location, 
# next specify output of resample folder location, 
# finally list final table location of table
pathlist = [r"F:\TimData\DataTests\CRUZonalStats\pet" + "\\", 
            r"F:\TimData\DataTests\CRUZonalStats\pet_clip" + "\\",
            r"F:\TimData\DataTests\CRUZonalStats\pet_resample" + "\\",
            r"F:\TimData\DataTests\CRUZonalStats\pet_zonalstats" + "\\"]


def makefiles():
    '''create folders if they do not already exist
    '''
    for files in pathlist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  
            
            
def dissolveAndBuffer(poly):
    '''Dissolve polygon, then create buffer around polygon for clipping later
    '''
    dissoutname = "US_county_diss.shp" # output name of dissolved polygon 
    arcpy.Dissolve_management(pathlist[0]+poly, pathlist[0]+dissoutname)
    print "Finished dissolving polygon before buffering"
    buffoutname = "US_county_buff.shp" # output name of buffer polygon 
    arcpy.Buffer_analysis(pathlist[0]+dissoutname, pathlist[0]+buffoutname, 
                          "60 Kilometers", "#", "#", "ALL")
    print "Finished adding 60km buffer to polygon"
    return buffoutname


def clipRasters(buffpoly):
    '''clip all rasters to buffer, copy to new folder'''
    env.workspace = pathlist[0] # Workplace for rasters 
    raslist = arcpy.ListRasters() # create raster list of all rasters 
    for ras in raslist: # iterate through rasters 
        #define output name
        startname = str(ras) + "_clip.tif"
        name = startname.replace(".asc", "") 
        arcpy.Clip_management(ras, "#", pathlist[1]+name, buffpoly, "#", 
                              "ClippingGeometry", "NO_MAINTAIN_EXTENT")
        # keep track of processing
        print "Clipping", name, "complete."
        

def resample():
    '''resample all clipped rasters to resolution of ~1km2'''
    env.workspace = pathlist[1] # Workplace for clipped rasters 
    raslist = arcpy.ListRasters() # create raster list of all rasters 
    for ras in raslist: # iterate through rasters 
        #define output name
        startname = str(ras) + "_res.tif"
        name = startname.replace("_clip.tif", "") 
        arcpy.Resample_management(ras, pathlist[2]+name, "0.00833", "#")
        # keep track of processing
        print "Resampling", name, "complete."

    
def zonalstats(poly, polycolumn, stat):
    '''Run zonal stats on every clipped and resampled raster in folder for the 
       polygon, polygon column, and stats specified
    '''
    # Set workplace for rasters and admin polygon  
    env.workspace = pathlist[2]
    # create raster list of all rasters 
    raslist = arcpy.ListRasters()
    # set count for adding to the end of zonal stats table name  
    count = 1
    #iterate through rasters 
    for ras in raslist: 
        #define output name, make sure out tables are sorting correctly
        if count <10:
            name = "a_ZonalStats" + str(count) + ".dbf"
        elif count <100:
            name = "b_ZonalStats" + str(count) + ".dbf"
        elif count <1000:
            name = "c_ZonalStats" + str(count) + ".dbf"
        else:
            name = "d_ZonalStats" + str(count) + ".dbf"
        outZSat = ZonalStatisticsAsTable(pathlist[0]+poly, polycolumn, ras, 
                                         pathlist[3]+name, "DATA", stat)
        #keep track of processing
        print "Processing", name, "complete."
        count = count + 1


def copyShapefiles(poly,count):
    '''Make copies of shapefile, to append results to
    '''
    env.workspace = pathlist[0] # path of shapefile
    name = "US_county_" + str(count) + ".shp"
    arcpy.CopyFeatures_management(poly, pathlist[0]+name)
    print "Copied", name
    return name 


def combinetables(poly, polycolumn, stat, startindex, endindex):
    '''Merge tables together and add to table in shapefile. 
       Startindex and endindex defines the indexing to use on tablelist to 
       make sure only 240 (1200/5) columns are added to each shapefile.
       Column in polygon is set to merge tables on, statistic is used to define
       column of interest to keep.
    '''
    env.workspace = pathlist[3] # workplace where tables are located 
    tablelist = arcpy.ListTables() # list tables in file
    indxtablelist = tablelist[startindex:endindex] # index tablelist
    # combine tables so they are located in shapefile based on common attribute
    for table in indxtablelist:
        arcpy.JoinField_management (pathlist[0] + poly, polycolumn, table, 
                                    polycolumn, [stat])
        #keep track of processing
        print "Combining", table, "table complete."


def main():
    '''Run zonal stats and combinetables Function
    '''
    #name admin poly 
    adminpoly = "US_county.shp"
    #name admin polygon column of interest (ex: state, county, country, etc..)
    adminpolycolumn = "FIPS"
    #name statistic of interest in all caps 
    zonalstat = "MEAN"
    
    makefiles() # make files if they don't exist
    buffpoly = dissolveAndBuffer(adminpoly) # dissolve and buffer shapefile
    clipRasters(buffpoly) # use returned bufferpoly to clip raster with 
    resample() # resample all rasters 
    zonalstats(adminpoly, adminpolycolumn, zonalstat) # zonal stats of rasters 
    
    # make copies of shapefiles
    adminpoly2 = copyShapefiles(adminpoly,2)
    adminpoly3 = copyShapefiles(adminpoly,3)
    adminpoly4 = copyShapefiles(adminpoly,4)
    adminpoly5 = copyShapefiles(adminpoly,5) 
    
    env.workspace = pathlist[3] # workplace where tables are located 
    tablelist = arcpy.ListTables() # list tables in file to get length of list
    fifthlist = int(len(tablelist)/5) #get 5th size of list
    #copy tables to the 5 different shapefiles. 
    combinetables(adminpoly, adminpolycolumn, zonalstat, 0, fifthlist)
    combinetables(adminpoly2, adminpolycolumn, zonalstat, 
                  fifthlist, fifthlist*2)
    combinetables(adminpoly3, adminpolycolumn, zonalstat, 
                  fifthlist*2, fifthlist*3)
    combinetables(adminpoly4, adminpolycolumn, zonalstat, 
                  fifthlist*3, fifthlist*4)
    combinetables(adminpoly5, adminpolycolumn, zonalstat, 
                  fifthlist*4, len(tablelist))
    
      
if __name__ =="__main__":
    main()
    
    
#Print out time of finish
print (time.time() - start_time)/60, "minutes, finished"    
    
    
    
    