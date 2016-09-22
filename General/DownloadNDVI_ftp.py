'''
Created on Apr 8, 2016

@author: TIMOTHYJOHNSON

This script is used to download NDVI files from a NOAA ftp location. There are 
several weekly files, but I am only interested in the NDVI ones, which 
end in "SM.SMN.tif".
'''

import time, os
from ftplib import FTP

start_time = time.time() # start time

os.chdir(r"F:\TimData\Liang\Malawai\NDVI"+ "\\")


def NDVIdownload():
    url = 'ftp.star.nesdis.noaa.gov'
    ftp = FTP(url)
    ftp.login()
    ftp.cwd('/pub/corp/scsb/wguo/data/VHP_4km/geo_TIFF')
    files = ftp.nlst() # get list of files at ftp folder location
    files.sort()
    for f in files:
        if f.endswith("SM.SMN.tif"): # only download NDVI files
            ndvifile=open(f,"wb")
            ftp.retrbinary('RETR %s' % f, ndvifile.write) # download file
            print "Downloaded", f
            ndvifile.close()   
    ftp.close()
   
   
def main():
    NDVIdownload()        


#execute main if code is run
if __name__ == "__main__": 
    main()        
    
#Print out time of finish and verify success of finish
print (time.time() - start_time) / 60, "minutes, finished"  