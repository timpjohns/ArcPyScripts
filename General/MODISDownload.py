'''
Created on May 28, 2015

@author: timothyjohnson
'''
#This script is used for downloading multiple modis tiles from online. First the data is downloaded from the Reverb ECHO website. The output
# is a text file with http web addresses listed, one per line. When the address is accessed download begins immediately on browser. 

from __future__ import division
import urllib as url
import time
import os

#start time
start_time = time.time()

#set path to folder containing text file
path = r"F:\TimData\MODISLandCover"

#read text file
httpfile = open(path + r'//' + 'data_url_script_2015-05-28_141457.txt')

#keep count to keep track of files
count = 0

def httpdownload():
    #loop through each line in the text file
    for line in httpfile:
        #create name of files
        nametest = str(count) + ".hdf"
        #open url file
        openurl = url.URLopener()
        #save file to path with name
        linefile = openurl.retrieve(line, path + r'//' + nametest)
        #keep track of progress
        print line + " finished"
        #add 1 to count to keep track of files
        count = count + 1 

def main():
    httpdownload()        

#execute main if code is run
if __name__ == "__main__": 
    main()        
    
#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"    
    
    
    