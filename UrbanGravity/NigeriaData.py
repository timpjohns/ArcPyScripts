'''
Created on Aug 12, 2015

@author: TIMOTHYJOHNSON

This script is for working with Urban Night time DSMP lights in Nigeria. The average lights X pct data from 1992-2009 are 
downloaded from http://ngdc.noaa.gov/eog/dmsp/downloadV4composites.html. It is then clipped to Nigeria, calibration 
equations are run, and the data is adjusted for growth -by taking the average of forward and backward adjustments. 
The methodology for calibration and growth adjustment is taken from the "Correcting Incompatible DN Values and Geometric 
Errors in Nighttime Lights Time Series Images" article. Calibration equations for the years 1992-2009 are taken from the 
article: Elvidge, et al. 2011 "National trends in Satellite Observed Lighting:1992-2009". The data is first clipped to 
Nigeria, using the most recent GAULAdmin data for Nigeria. Then the calibration equations are used. Next the forward 
and backward adjusts are made, averaging the results. After this, pixels below 2.5 are set to null. And, finally, the pixels 
are summed for each state in Nigeria and merged into the GAULAdmin shapefile table.
'''

#Import system modules
from __future__ import division
import arcpy
from arcpy import env
from arcpy.sa import *
import time
import os, sys
import smtplib

# start time to calculate time script takes to run
start_time = time.time()

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# create list of file locations to save outputs
filelist = [r"F:\TimData\UrbanGravity\NigeriaData\pctlightDMSPdata\1992to2009" + "\\", 
            r"F:\TimData\UrbanGravity\NigeriaData" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\clipped" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\calibrated" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\Adjustment\backward" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\Adjustment\forward" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\Adjustment\average" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\threshold" + "\\",
            r"F:\TimData\UrbanGravity\NigeriaData\pixelSum" + "\\"]


def makefiles():
    """create folders if they do not already exist"""
    for files in filelist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  

            
def cliprasters():
    """Clips rasters from years 1992-2009 to Nigeria GAUL admin boundary"""
    env.workspace = filelist[0]
    #create raster list to iterate through 
    raslist = arcpy.ListRasters()    
    for ras in raslist:
        # Define name and location of output data
        name = str(ras)+ "_clip.tif"
        # Execute set null
        arcpy.Clip_management(ras, "#" , filelist[2] + name, filelist[1]+ "NigeriaGAULAdmin_states.shp", "255", "ClippingGeometry", "MAINTAIN_EXTENT")
        #keep track of rasters completed
        print "processing " + ras + "completed clip"


def calibrationeq():
    """Use calibration equation on rasters already clipped to Nigeria
    """
    # Set initial workplace
    env.workspace = filelist[2]
    #list of values to use in calculations
    C0 = [-0.1068, -0.2477, 0.1651, 0.4104, 0.2228, -0.0008, 0.1536, -0.1675, 0.1061, -0.2596, 0.4486, -0.2767,\
          -0.4436, -0.2375, 0.0287, 0.3211, -0.1203, 0.3500]
    C1 = [1.4361, 1.5203, 1.1244, 1.2116, 1.2700, 1.1652, 1.0452, 1.5116, 1.3878, 1.3467, 1.1983, 1.2840,\
          1.2081, 1.4250, 1.1339, 0.9217, 1.0155, 1.0883]
    C2 = [-0.0068, -0.0081, -0.0019, -0.0035, -0.0041, -0.0024, -0.0010, -0.0079, -0.0060, -0.0053, -0.0035, -0.0044,\
          -0.0031, -0.0064, -0.0014, 0.0013, -0.0002, -0.0016]
    # create list of nighttime light rasters from 1992-2009 so that they can be iterated through 
    ras_list = arcpy.ListRasters()
    #keep track of files and list locations
    count=0
    #raster calculation
    for ras in ras_list:
        # Define name and location of output data
        name = str(ras)+ "_calibrated.tif"
        # Execute calculation
        out = C0[count] + (Raster(ras) * C1[count]) + ((Raster(ras)^2) * C2[count]) 
        out.save(filelist[3] + name)
        count = count+1
        print "Finished calibrating " + str(ras)

def copyraster(fileloc):
    """Define function to copy raster to another file location for future use in mosaic function"""
    env.workspace = filelist[3]
    # create raster list to grab raster of interest to copy for mosaic 
    ras_list = arcpy.ListRasters()
    print str(ras_list[len(ras_list)-1])
    if fileloc ==4:
        #copy first raster of last date, 2009, to mosaic later in the output location
        arcpy.Copy_management(ras_list[len(ras_list)-1], filelist[fileloc] + ras_list[len(ras_list)-1]) 
        print "copied 2009 raster"
    else:
        #copy first raster of first date, 1992, to mosaic later in the output location
        arcpy.Copy_management(ras_list[0], filelist[fileloc] + ras_list[0]) 
        print "copied 1992 raster"
       
def backwardadjustment():
    """sets the previous years values to the current if the previous year has greater values than the current.
       Works backwards starting by comparing 2008 and 2009 by reversing list and ending with 1992 unchanged"""
    # Set initial workplace
    env.workspace = filelist[3]
    # set count to keep track of place in list during iteration 
    mergeindex = 0
    # set name count for merging 
    count = 2008
    #set place for raster list
    place = 1 
    # create list of nighttime light rasters from 1992-2009 so that they can be iterated through 
    ras_list = arcpy.ListRasters()
    #reverses raster list to start by comparing 2008 and 2009
    newlist = ras_list[::-1]
    print "Here is the reversed raster list: " + str(newlist)
    #create initial list where mosaiced rasters will go to mosaic to the next raster. Start with 2009. Make sure it calls to right folder
    mergelist = [newlist[0]]
    while count > 1991:
        #set first raster to mosaic to the first raster in mergelist
        inras1 = filelist[4]+mergelist[mergeindex]
        #set second raster to mosaic as county1 variable, which will be moved to next location in list each iteration
        inras2 = newlist[place]
        #add input rasters along with ";" separator due to finicky nature of "mosaic to new raster" tool 
        finalras = inras1+";"+inras2
        #make sure correct rasters are being mosaiced each iteration
        print finalras
        # Define name and location of output data.
        startname = str(newlist[place])+ "_backwardAdj.tif"
        name = startname.replace("_clip.tif_calibrated.tif_setnull.tif", "") 
        #run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras, filelist[4], name, '#', '32_BIT_FLOAT', '#', "1", "MINIMUM", '#')
        print "Finished doing backward adjustment, created new " + str(count) + " raster"
        #append output to first location in mergelist to use in next iteration
        mergelist.insert(0, name)
        #add 1 to county and count variables to move location in lists
        count = count - 1      
        place = place + 1 
        print "This is the merge list: " + str(mergelist)

    
def forwardadjustment():
    """sets the current years values to that of the previous years if the previous years is greater than the current.
       Works forward starting at comparing 1992 and 1993 and leaves 2009 unchanged"""
    # Set initial workplace
    env.workspace = filelist[3]
    # set count to keep track of place in list during iteration 
    mergeindex = 0
    # set name count for merging 
    count = 1993
    #set place for raster list
    place = 1 
    # create list of nighttime light rasters from 1992-2009 so that they can be iterated through 
    ras_list = arcpy.ListRasters()
    #create initial list where mosaiced rasters will go to mosaic to the next raster
    mergelist = [ras_list[0]]
    while count < 2010:
        #set first raster to mosaic to the first raster in mergelist
        inras1 = filelist[5]+mergelist[mergeindex]
        #set second raster to mosaic as county1 variable, which will be moved to next location in list each iteration
        inras2 = ras_list[place]
        #add input rasters along with ";" separator due to finicky nature of "mosaic to new raster" tool 
        finalras = inras1+";"+inras2
        #make sure correct rasters are being mosaiced each iteration
        print finalras
        # Define name and location of output data.
        startname = str(ras_list[place])+ "_forwardAdj.tif"
        name = startname.replace("_clip.tif_calibrated.tif_setnull.tif", "") 
        #run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras, filelist[5], name, '#', '32_BIT_FLOAT', '#', "1", "MAXIMUM", '#')
        print "finished merging datasets, created new " + str(count) + " raster"
        #append output to first location in mergelist to use in next iteration
        mergelist.insert(0, name)
        #add 1 to county and count variables to move location in lists
        count = count + 1      
        place = place + 1 
  
    
def averageadj():
    """averages the results from backward and forward adjustment"""
    # Set workplace of backward adjustment, remove 1992 and 2009 from list since it is not included in forward adjustment 
    env.workspace = filelist[4]
    raslist1 = arcpy.ListRasters()
    newraslist1 = raslist1[1:len(raslist1)-1]
    print str(newraslist1)
    
    # Set workplace of forward adjustment, remove 2009 from list since it is not included in backward adjustment 
    env.workspace = filelist[5]
    raslist2 = arcpy.ListRasters()
    newraslist2 = raslist2[1:len(raslist1)-1]
    print str(newraslist2)
    
    #set count for keeping track of place in raster list 
    count = 0 
    for ras in newraslist2:
        #set first raster to mosaic to the first raster in mergelist
        inras1 = filelist[4]+newraslist1[count]
        #set second raster to mosaic as county1 variable, which will be moved to next location in list each iteration
        inras2 = ras
        #add input rasters along with ";" separator due to finicky nature of "mosaic to new raster" tool 
        finalras = inras1+";"+inras2
        #make sure correct rasters are being mosaiced each iteration
        print finalras
        # Define name of output data.
        name = str(ras)+ "_averageOfAdj.tif"
        #run mosaic tool
        arcpy.MosaicToNewRaster_management(finalras, filelist[6], name, '#', '32_BIT_FLOAT', '#', "1", "MEAN", '#')
        print "finished averaging adjusted raster " + str(ras) + " raster"
        count = count + 1 
    

def threshold(fileloc):
    """Sets all values less than 2.5 to null, following the methodology of the 2015 calibration article.
       Takes folder location as input, since 1992 and 2009 will be located in different folders
    """
    # Set initial workplace
    env.workspace = filelist[fileloc]
    if fileloc ==6:
        # create list of nighttime light rasters from 1992-2009 so that they can be iterated through 
        ras_list = arcpy.ListRasters()
        #run loop so that values <2.5 are null   
        for ras in ras_list:
            # Define name and location of output data
            name = str(ras)+ "_setnull.tif"
            outsetnull = SetNull(ras, ras, "VALUE < 2.5")
            outsetnull.save(filelist[7]+name)      
            print "Finished applying threshold for " + str(ras)  
    elif fileloc ==5:
        # create list of nighttime light rasters, but only use 2009 for forward adjustment 
        Origraslist = arcpy.ListRasters()
        ras = Origraslist[len(Origraslist)-1]
        name = str(ras)+ "_setnull.tif"
        outsetnull = SetNull(ras, ras, "VALUE < 2.5")
        outsetnull.save(filelist[7]+name)
        
    elif fileloc ==4:
        # create list of nighttime light rasters, but only use 1992, for backwards adjustment 
        Origraslist = arcpy.ListRasters()
        ras = Origraslist[0]
        name = str(ras)+ "_setnull.tif"
        outsetnull = SetNull(ras, ras, "VALUE < 2.5")
        outsetnull.save(filelist[7]+name)

    
def zonalstatsSum():
    """Takes the pixel sum of all pixels in each state of Nigeria"""  
    # Set workplace for average adjusted and calibrated rasters
    env.workspace = filelist[7]
    raslist = arcpy.ListRasters()
    # set variable names for keeping track of filename
    count = 1992
    for ras in raslist:
        #define output name
        name = str(count) + "_ZonalSum_Nigeria.dbf"
        outZSat = ZonalStatisticsAsTable(filelist[1]+ "NigeriaGAULAdmin_states.shp", "ADM1_NAME", ras, filelist[8] + name, "DATA", "SUM")
        #keep track of processing
        print " \n Processing " + str(count) + " complete. Finished doing zonal stats"
        count = count + 1

    
def mergetable():
    """merges all table results from zonal stats. Add output to admin shapefiles table"""
    # Set new workplace where tables are located 
    env.workspace = filelist[8]
    # list tables in file
    tablelist = arcpy.ListTables()   
    # combine tables so they are all located in shapefile based on common attribute
    for table in tablelist:
        arcpy.JoinField_management (filelist[1]+ "NigeriaGAULAdmin_states.shp", "ADM1_NAME", table, "ADM1_NAME", ["SUM"])
        #keep track of processing
        print "processing " + table + " complete"  


def sendtext(successorfail):
    """sends text of whether program succeeds or fails
       takes the succeed or fail message as input depending on if error occurs. Removed my info to make public"""
    #My gmail info   
    sender = ''
    receiver = ''
    password = "" 
    message = successorfail 
    #If properly connected to gmail print success, otherwise print failure.  
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        #server_ssl.ehlo() # optional, called by login()
        server_ssl.login(sender, password)  
        server_ssl.sendmail(sender, receiver, message)
        server_ssl.close()
        print "successfully sent message"  
    except:
        print "Error in sending text message"   


def main():
    """Mostly just implements functions. Includes try statement to determine which text message to send"""
    try:
        makefiles()
        print "\nFinished making folders.\n"
        cliprasters()
        print "\nFinished clipping rasters.\n"
        calibrationeq()
        print "\nFinished calibrating rasters.\n"
        copyraster(4)
        print "\nFinished copying raster for backward calibration.\n"
        copyraster(5)
        print "\nFinished copying raster for forward calibration.\n"
        backwardadjustment()
        print "\nFinished doing backward pixel adjustment.\n"
        forwardadjustment()
        print "\nFinished doing forward pixel adjustment.\n"
        averageadj()
        print "\nFinished averaging adjustment.\n"
        #Run threshold function for different folder locations
        threshold(6)
        print "\nFinished applying threshold values for average adjusted rasters.\n"
        #threshold(5)
        #print "\nFinished applying threshold values for 2009.\n"
        #threshold(4)
        #print "\nFinished applying threshold values for 1992.\n"
        zonalstatsSum()
        print "\nFinished doing zonal stats.\n"
        mergetable()
        print "\nFinished merging tables.\n"
        sendtext("""Program finished successfully""")             
    except Exception as e:
        print e.message
        print 'Error occurred on line {}'.format(sys.exc_info()[-1].tb_lineno)
        sendtext("""Program failed, terribly sorry""") 
                       
#execute main if code is run
if __name__ == "__main__": 
    main()

#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"        

        
        
