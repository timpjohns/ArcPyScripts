'''
Created on July 7, 2016

@author: TIMOTHYJOHNSON

Iterates through monthly TAMSAT netcdf files from 1983-present, converts them
to raster, does zonal stats to dbf table, converts dbf files to csvs, 
stacks csvs to one file, and then adds a time column based on time contained 
in TAMSAT file names. 
'''

# Import system modules
from __future__ import division
import arcpy
import os, time, csv
import glob 
import pandas as pd
from arcpy import env
from arcpy.sa import *
from dbfpy import dbf

# start time to keep track of time 
start_time = time.time()

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

pathlist = [r"D:\CopiedData\CopySIF\SIF_Proposal\TAMSAT\TotalNCFiles" + "\\",
            r"D:\CopiedData\CopySIF\SIF_Proposal\TAMSAT\TotalNCFiles\zonal2" + "\\",
            r"D:\CopiedData\CopySIF\SIF_Proposal" + "\\"]


def makefiles():
    '''create folders if they do not already exist
    '''
    for files in pathlist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  

'''
def netcdftoRaster():
    #convert all netcdf files to raster to use as input to zonal stats
    #raslist = arcpy.ListRasters() # create raster list of all rasters
    netcdflist = glob.glob(pathlist[0] + "/*.nc") 
    for nc in netcdflist:  
        #define output name
        outname1 = str(nc).replace(".nc", "")
        outname = outname1 + ".tif"
        arcpy.MakeNetCDFRasterLayer_md(nc, "rfe", "lon", "lat", outname1)
        arcpy.CopyRaster_management(outname1, outname)
        print "Completed converting netcdf to raster for:", outname      
'''           
                      
def zonalstats():
    '''Run zonal stats to table on every TAMSAT raster
    '''
    env.workspace = pathlist[0] # Set workplace for rasters
    raslist = arcpy.ListRasters()
    for ras in raslist:  
        #define output name
        outname1 = str(ras).replace(".tif", "")
        outname = outname1 + ".dbf"
        outZSat = ZonalStatisticsAsTable(pathlist[2]+
                                         "StudyCountries_07_07_2016_SecHalf.shp", 
                                         "FID", ras, pathlist[1]+outname, 
                                         "DATA", "MEAN")
        print "Completed", outname


def DBFtoCSV():
    '''Convert every DBF table into CSV table. 
    '''
    env.workspace = pathlist[1] # Set new workplace where tables are located 
    tablelist = arcpy.ListTables() # list tables in file
    for table in tablelist: # iterate through every table
        #make sure you are just working with .dbf tables 
        if table.endswith('.dbf'):
            #name csv the same as the .dbf table just with .csv at the end
            csv_fn = table[:-4]+ ".csv"
            with open(pathlist[1]+csv_fn,'wb') as csvfile: # name output path
                in_db = dbf.Dbf(pathlist[1]+table)
                out_csv = csv.writer(csvfile)
                #copy row names and items in rows from dbf to csv
                names = []
                for field in in_db.header.fields:
                    names.append(field.name)
                out_csv.writerow(names)
                for rec in in_db:
                    out_csv.writerow(rec.fieldData)
                in_db.close()
        #keep track of processing
        print "Completed", table[:-4]+".csv table."


def stackdata():
    '''stack all csv files'''
    alltxts = glob.glob(pathlist[1] + "/*.csv")
    firsttxt =  alltxts[:1] # text to append the others to
    totaldf = pd.read_csv(firsttxt[0])
    testtxts = alltxts[1:]
    for txt in testtxts:
        df = pd.read_csv(txt)
        totaldf = totaldf.append(df)
        print "Finished", txt
    print totaldf
    return totaldf  
    
    
def addDateColumn(csvfile):
    """Adds year and month for each raster to new column year 
    """
    # read csv file 
    df = pd.read_csv(pathlist[0] + csvfile)
    env.workspace = pathlist[0] # Set workplace for rasters to get names
    raslist = arcpy.ListRasters() # create raster list of all rasters 
    newyears = [] # create new empty column to append times to
    for ras in raslist:
        print ras[3:-4]
        newyears.append(ras[3:-4]) # append just date information in file name    
    newtime = [] # empty list to append repeating times for different rows
    toiterate = df[df.columns[0]] # ID of districts to base repeating times
    print "First column:", toiterate
    count = 0 # for indexing item in time list 
    for i in toiterate[1:]: # remove first zero and add time value later
        if i !=0:
            newtime.append(newyears[count])
        else:
            count+=1
            newtime.append(newyears[count])
    newtime.insert(0,"1983_02")
    print newtime 
    print len(newtime)
    
    df["time"] = newtime #create new column in dataframe based on repeating time
    df.to_csv(pathlist[0] + 'TotalStackedTAMSATData_time2.csv')

                          
def main():
    makefiles()
    #netcdftoRaster()
    zonalstats()
    DBFtoCSV()
    totalcsv = stackdata()
    totalcsv.to_csv(pathlist[0] + 'TotalStackedTAMSATData2.csv')
    addDateColumn('TotalStackedTAMSATData2.csv')
    
    
if __name__ =="__main__":
    main()
    
    
print time.time() - start_time, "seconds, finished" # Print out time of finish 