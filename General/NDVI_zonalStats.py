'''
Created on May 24, 2016

@author: TIMOTHYJOHNSON

Iterates through weekly NDVI rasters from 1981-2016, does zonal stats to dbf 
table, converts dbf files to csvs, stacks csvs to one file, and then adds a 
time column based on time contained in ndvi raster file names. 
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

pathlist = [r"F:\TimData\Liang\Malawai\NDVI\Setnull_global" + "\\",
            r"D:\CopiedData\CopySIF\SIF_Proposal\NDVI\ZonalStats2" + "\\",
            r"D:\CopiedData\CopySIF\SIF_Proposal" + "\\",
            r"D:\CopiedData\CopySIF\SIF_Proposal\NDVI" + "\\"]


def makefiles():
    '''create folders if they do not already exist
    '''
    for files in pathlist:
        if not os.path.exists(files): 
            os.makedirs(files)
            print "made " + files  
      
      
def zonalstats():
    '''Run zonal stats to table on every ndvi raster
    '''
    env.workspace = pathlist[0] # Set workplace for ndvi rasters
    raslist = arcpy.ListRasters() # create raster list of all rasters 
    for ras in raslist[1223:]:  
        #define output name
        outname1 = str(ras).replace(".", "")
        outname2 = outname1.replace("SMSMNtif_setnulltif", "")
        outname3 = outname2.replace("VHPG04C07", "")
        outname = outname3 + ".dbf"
        outZSat = ZonalStatisticsAsTable(pathlist[2]+"StudyCountries_07_07_2016_SecHalf.shp", 
                                         "FID", ras, pathlist[1]+outname, 
                                         "DATA", "MEAN")
        print "Completed zonal stats on:", outname


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
    df = pd.read_csv(pathlist[3] + csvfile)
    env.workspace = pathlist[0] # Set workplace for ndvi rasters to get names
    raslist = arcpy.ListRasters() # create raster list of all rasters 
    newyears = [] # create new empty column to append times to
    for ras in raslist:
        newyears.append(ras[16:-11]) # append just date information in file name
    newtime = [] # empty list to append repeating times for different rows
    toiterate = df[df.columns[0]] # ID of districts to base repeating times
    count = 0 # for indexing item in time list 
    for i in toiterate[1:]: # remove first zero and add time value later
        if i !=0:
            newtime.append(newyears[count])
        else:
            count+=1
            newtime.append(newyears[count])
    newtime.insert(0,"1981035")
    print len(newtime)

    df["time"] = newtime #create new column in dataframe based on repeating time
    df.to_csv(pathlist[3] + 'TotalStackedNDVIData_time2.csv')

                          
def main():
    makefiles()
    zonalstats()
    DBFtoCSV()
    totalcsv = stackdata()
    totalcsv.to_csv(pathlist[3] + 'TotalStackedNDVIData2.csv')
    addDateColumn('TotalStackedNDVIData2.csv')
    
    
if __name__ =="__main__":
    main()
    
    
print time.time() - start_time, "seconds, finished" # Print out time of finish  
