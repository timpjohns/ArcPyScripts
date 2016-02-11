'''
Created on Feb 3, 2016

@author: timothyjohnson

This script is for working with Urban Night time DSMP lights. The average lights 
from 1992-2013 are downloaded from 
http://ngdc.noaa.gov/eog/dmsp/downloadV4composites.html. The methodology for 
calibration is taken from the article: "Correcting Incompatible DN Values and 
Geometric Errors in Nighttime Lights Time Series Images".
1) Calibration equations for the years 1992-2009 are taken from the article: 
Elvidge, et al. 2011 "National trends in Satellite Observed Lighting:1992-2009".
2010-2013 do not have a calibration performed since the data is not available. 
The same sensor, F18, is available for 2010-2013 which is used to keep the later 
dates as consistent as possible. The forward and backward adjustments for growth 
include all dates, so 2010-2013 are adjusted going off of the calibration 
equation used for 1992-2009. 
2) Forward adjustments are then made, which assume growth is occurring. If the 
next years pixel is less than the previous, it increases the value of the next
years pixel to that of the previous one. 
3) Backward adjustments are then done because forward adjustment increases or 
keeps all pixels the same based on the first years values, the opposite is done 
working backwards starting at 2013. 
4) Forward and Backward adjustments are then averaged.
5) Finally, pixels below 2.5 are set to null. 
'''


# Import system modules
from __future__ import division
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import os


# start time to calculate time script takes to run
start_time = time.time()

arcpy.env.overwriteOutput = True # Overwrite pre-existing files

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# create list of file locations to save outputs
filelist = [r"F:\TimData\UrbanGravity\UrbanGravityNightlightPaper" \
            r"\Calibrated_Global_NLs\lightDMSPdata" + "\\",
            r"F:\TimData\UrbanGravity\UrbanGravityNightlightPaper" \
            r"\Calibrated_Global_NLs\calibrated" + "\\",
            r"F:\TimData\UrbanGravity\UrbanGravityNightlightPaper" \
            r"\Calibrated_Global_NLs\backward" + "\\",
            r"F:\TimData\UrbanGravity\UrbanGravityNightlightPaper" \
            r"\Calibrated_Global_NLs\forward" + "\\",
            r"F:\TimData\UrbanGravity\UrbanGravityNightlightPaper" \
            r"\Calibrated_Global_NLs\average" + "\\",
            r"F:\TimData\UrbanGravity\UrbanGravityNightlightPaper" \
            r"\Calibrated_Global_NLs\threshold" + "\\"]

#raster to use for snapping 
snapraster = filelist[0]+"F101992.v4b_web.stable_lights.avg_vis.tif"

def makefiles():
    """create folders if they do not already exist"""
    for files in filelist:
        if not os.path.exists(files):
            os.makedirs(files)
            print "made", files

     
def calibrationeq():
    """Use calibration equation for rasters 1992-2009
    """
    env.workspace = filelist[0] # Set initial workplace
    # list of values to use in calculations
    C0 = [-0.1068, -0.2477, 0.1651, 0.4104, 0.2228, -0.0008, 0.1536, -0.1675, 
          0.1061, -0.2596, 0.4486, -0.2767, -0.4436, -0.2375, 0.0287, 0.3211, 
          -0.1203, 0.3500]
    C1 = [1.4361, 1.5203, 1.1244, 1.2116, 1.2700, 1.1652, 1.0452, 1.5116, 
          1.3878, 1.3467, 1.1983, 1.2840, 1.2081, 1.4250, 1.1339, 0.9217, 
          1.0155, 1.0883]
    C2 = [-0.0068, -0.0081, -0.0019, -0.0035, -0.0041, -0.0024, -0.0010, 
          -0.0079, -0.0060, -0.0053, -0.0035, -0.0044, -0.0031, -0.0064, 
          -0.0014, 0.0013, -0.0002, -0.0016]
    
    ras_list = arcpy.ListRasters() # list rasters from 1992-2009
    #subtract 4 from 1992-2013 list to get 1992-2009
    newraslist = ras_list[:-4]
    print str(newraslist) # test check
    count = 0 # keep track of files and list locations
    for ras in newraslist:
        # Define name and location of output data
        name = str(ras) + "_calibrated.tif"
        arcpy.env.snapRaster =snapraster #Snap rasters 
        # Execute calculation
        out = C0[count] + (Raster(ras) * C1[count]) + \
            ((Raster(ras) ^ 2) * C2[count])
        out.save(filelist[1] + name)
        count = count + 1
        print "Finished calibrating " + str(ras)
        
                
def copyraster(fileloc):
    """Copy raster to another file location for future use in mosaic function. 
       fileloc determines where to copy raster.
    """
    arcpy.env.snapRaster = snapraster # Snap raster
    if fileloc == 2:
        env.workspace = filelist[1]
        # create raster list to grab raster of interest to copy for mosaic
        ras_list = arcpy.ListRasters()
        # copy first raster 2013, to mosaic later in the output location
        arcpy.Copy_management(ras_list[len(ras_list) -1], filelist[fileloc] + 
                              ras_list[len(ras_list) -1])
        print "copied 2013 raster"
    elif fileloc ==3:
        env.workspace = filelist[1]
        # create raster list to grab raster of interest to copy for mosaic
        ras_list = arcpy.ListRasters()
        # copy first raster 1992 to mosaic later in the output location
        arcpy.Copy_management(ras_list[0], filelist[fileloc] + ras_list[0])
        print "copied 1992 raster"
    else:
        # copy rasters 2010-2013 that didn't get calibrated to calibrated folder
        env.workspace = filelist[0]
        # create raster list to grab raster of interest to copy for mosaic
        ras_list = arcpy.ListRasters()
        # last 4 rasters
        last4ras = ras_list[len(ras_list)-4:len(ras_list)]
        for ras in last4ras:
            # copy rasters 2010-2013 to calibration folder
            arcpy.Copy_management(ras, filelist[1] + ras)
            print "copied", ras, "to calibration folder"
        

def backwardadjustment(dates = "all"):
    """sets the previous years values to the current if the previous year has 
       greater values than the current. Works backwards starting by comparing 
       2012 and 2013 by reversing list and ending with 2013 unchanged. After 
       forward and backward adjustments are completed results are averaged and 
       1992 is calibrated using the 1993 average, by changing the 
       dates function input variable
    """
    arcpy.env.snapRaster = snapraster # Snap raster
    if dates =="all":
        # Set initial workplace
        env.workspace = filelist[1]
        # set count to keep track of place in list during iteration
        mergeindex = 0
        count = 2012 # set name count for merging
        place = 1 # set place for raster list
        ras_list = arcpy.ListRasters() # create list of rasters
        # reverses raster list to start by comparing 2012 and 2013
        newlist = ras_list[::-1]
        print "Here is the reversed raster list: " + str(newlist) #test check 
        # create list where mosaiced rasters will go to mosaic to the next
        # raster. Start with 2013. Make sure it calls to right folder
        mergelist = [newlist[0]]
        while count > 1991: 
            # set first raster to mosaic to the first raster in mergelist
            inras1 = filelist[2] + mergelist[mergeindex]
            #Snap all rasters to same cell alignment 
            arcpy.env.snapRaster = ras_list[0]
            # set second raster to mosaic as place variable, which will be moved
            # to next location in list each iteration
            inras2 = newlist[place]
            # add input rasters along with ";" separator due to finicky nature 
            # of "mosaic to new raster" tool
            finalras = inras1 + ";" + inras2
            # make sure correct rasters are being mosaiced each iteration
            print finalras
            # Define name and location of output data.
            startname = str(newlist[place]) + "_backwardAdj.tif"
            if "_calibrated.tif" in startname:
                name = startname.replace("_calibrated.tif", "")
            else:
                name = startname
            # run mosaic tool
            arcpy.MosaicToNewRaster_management(finalras,filelist[2],name,'#',
                                               '32_BIT_FLOAT','#',"1",
                                               "MINIMUM",'#')
            print "Finished doing backward adjustment on", str(count), "raster"
            # append output to first location in mergelist to use in next 
            # iteration
            mergelist.insert(0, name)
            # add 1 to place variable and subtract 1 to count to move list loc
            count = count - 1
            place = place + 1
            print "This is the mergelist: " + str(mergelist) # test check      
    else: # after 1993-2012 are averaged, now need to do backward calibration on 
        # just 1992
        env.workspace = filelist[0]# Set initial workplace of 1992 raster 
        #create raster list to get first item which is 1992
        Origraslist = arcpy.ListRasters()
        ras = Origraslist[0]
        # Set initial workplace of averaged 1993 raster
        env.workspace = filelist[4]
        #create raster list then specify first raster which is 1993
        Origraslist2 = arcpy.ListRasters()
        ras2 = Origraslist2[0]
        #add rasters together for input into mosaic tool 
        finalras = ras + ";" + ras2
        print finalras # test check 
        name = str(ras) + "_averageOfAdj.tif"
        # run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras,filelist[4],name,'#',
                                           '32_BIT_FLOAT','#',"1",
                                           "MINIMUM",'#')
        print "finished merging 1992 and 1993, created new", str(name), "raster"


def forwardadjustment(dates = "all"):
    """sets the current years values to that of the previous years if the 
       previous years is greater than the current. Works forward starting at 
       comparing 1992 and 1993 and leaves 1992 unchanged. After forward and 
       backward adjustments are completed results are averaged and 2013 is 
       calibrated using the 2012 average, by changing the dates function input 
       variable
    """
    arcpy.env.snapRaster = snapraster # Snap raster
    if dates =="all":
        env.workspace = filelist[1] # Set initial workplace
        mergeindex = 0 # Keep track of place in list during iteration
        count = 1993 # set count for merging
        place = 1 # set place for raster list
        ras_list = arcpy.ListRasters() # create raster list
        # create initial list where mosaiced rasters will go 
        mergelist = [ras_list[0]]
        while count < 2014:
            # set first raster to mosaic to the first raster in mergelist
            inras1 = filelist[3] + mergelist[mergeindex]
            # set second raster to mosaic based on place, moved to next location
            #  in list each iteration
            inras2 = ras_list[place]
            # add input rasters along with ";" separator due to finicky nature 
            # of "mosaic to new raster" tool
            finalras = inras1 + ";" + inras2
            print finalras # test check
            # Define name and location of output data.
            startname = str(ras_list[place]) + "_forwardAdj.tif"
            if "_calibrated.tif" in startname:
                name = startname.replace("_calibrated.tif", "")
            else:
                name = startname
            # run mosaic tool
            arcpy.MosaicToNewRaster_management(finalras,filelist[3],name,'#',
                                               '32_BIT_FLOAT','#',"1",
                                               "MAXIMUM",'#')
            print "finished merging datasets, created new", str(count), "raster"
            # append output to first location in mergelist for next iteration
            mergelist.insert(0, name)
            # add 1 to count and place variables to move location in lists
            count = count + 1
            place = place + 1
    else:
        env.workspace = filelist[0] # Set initial workplace of 2013 raster 
        Origraslist = arcpy.ListRasters() # Create list to get 2013 raster
        ras = Origraslist[len(Origraslist) - 1] # raster is last raster in list
        
        env.workspace = filelist[4] # Set initial workplace of 2012 raster
        Origraslist2 = arcpy.ListRasters() # Create list to get 2012 raster
        ras2 = Origraslist2[len(Origraslist2) - 1]# raster is last one in list 
        
        finalras = ras + ";" + ras2 # add inputs for mosaic to new raster tool
        print finalras # test check
        name = str(ras) + "_averageOfAdj.tif"
        # run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras,filelist[4],name,'#',
                                           '32_BIT_FLOAT','#',"1",
                                           "MAXIMUM",'#')
        print "finished merging 2012 and 2013, created new", str(name), "raster"
        

def averageadj():
    """averages the results from backward and forward adjustment"""
    arcpy.env.snapRaster = snapraster # Snap raster
    # Set workplace of backward adjustment, remove 1992 and 2013 from list
    # since they are not included in forward and backward adjustments
    env.workspace = filelist[2]
    raslist1 = arcpy.ListRasters()
    newraslist1 = raslist1[1:len(raslist1) - 1] # remove 1992 and 2013 from list
    print str(newraslist1) # test check
    # Set workplace of forward adjustment, remove 1992 and 2013 
    env.workspace = filelist[3]
    raslist2 = arcpy.ListRasters()
    newraslist2 = raslist2[1:len(raslist1) - 1] # remove 1992 and 2013 from list
    print str(newraslist2) # test check
    count = 0 # set count for keeping track of place in raster list
    for ras in newraslist2:
        # set rasters to average, keeping the same place in both lists of 
        # forward and backward adjusted rasters by count variable
        inras1 = filelist[2] + newraslist1[count]
        inras2 = ras
        # add input rasters along with ";" separator due to finicky nature of
        # "mosaic to new raster" tool
        finalras = inras1 + ";" + inras2
        print "These are the rasters being averaged:", finalras # test check
        # Define name of output data.
        name = str(ras) + "_averageOfAdj.tif"
        # run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras,filelist[4],name,'#',
                                           '32_BIT_FLOAT','#',"1","MEAN",'#')
        print "finished averaging adjusted raster", str(ras), "raster"
        count+=1 # add one to count, to match place in backward adj rasters


def threshold(fileloc):
    """Sets all values less than 2.5 to null, following the methodology of the 
       2015 calibration article. Takes folder location as input, since 1992 and 
       2013 will be located in different folders
    """
    arcpy.env.snapRaster = snapraster # Snap raster
    env.workspace = filelist[fileloc] # Set initial workplace
    if fileloc == 4:
        ras_list = arcpy.ListRasters() # list of avg rasters from 1993-2012
        for ras in ras_list:
            # Define name and location of output data
            name = str(ras) + "_setnull.tif"
            outsetnull = SetNull(ras, ras, "VALUE < 2.5") # set values <2.5 null
            outsetnull.save(filelist[5] + name)
            print "Finished applying threshold for", str(ras)
    elif fileloc == 3:
        # list of forward adjustment rasters, but only interested in 2013
        Origraslist = arcpy.ListRasters()
        ras = Origraslist[len(Origraslist) - 1]
        name = str(ras) + "_setnull.tif"
        outsetnull = SetNull(ras, ras, "VALUE < 2.5")
        outsetnull.save(filelist[5] + name)
        print "Finished applying threshold for", str(ras)
    elif fileloc == 2:
        # list of backward adjustment rasters, but only interested in 1992
        Origraslist = arcpy.ListRasters()
        ras = Origraslist[0]
        name = str(ras) + "_setnull.tif"
        outsetnull = SetNull(ras, ras, "VALUE < 2.5")
        outsetnull.save(filelist[5] + name)
        print "Finished applying threshold for", str(ras)
        
        
def main():
    """implements functions, with necessary parameters
    """
    makefiles()
    print "\nFinished making folders.\n"
    calibrationeq()
    print "\nFinished calibration equations.\n"
    copyraster(1)
    print "\nFinished copying 2010-2013 rasters.\n"
    copyraster(2)
    print "\nFinished copying raster for backward calibration.\n"
    copyraster(3)
    print "\nFinished copying raster for forward calibration.\n"
    backwardadjustment()
    print "\nFinished doing backward pixel adjustment.\n"
    forwardadjustment()
    print "\nFinished doing forward pixel adjustment.\n"
    averageadj()
    print "\nFinished averaging adjustment.\n"
    backwardadjustment("1992")
    print "\nFinished doing backward pixel adjustment for 1992.\n"
    forwardadjustment("2013")
    print "\nFinished doing forward pixel adjustment for 2013.\n"
    threshold(4)
    print "\nFinished applying threshold values for average adjusted rasters.\n"
    threshold(3)
    print "\nFinished applying threshold values for 2013.\n"
    threshold(2)
    print "\nFinished applying threshold values for 1992.\n"
    
    
if __name__ == "__main__":
    main()


print (time.time() - start_time) / 60, "minutes, finished"