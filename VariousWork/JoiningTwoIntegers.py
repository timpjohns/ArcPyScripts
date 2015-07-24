'''
Created on Jul 24, 2015

@author: TIMOTHYJOHNSON

Purpose: To add clairfying admin codes to the GADM shapefile, named UIDadmn1 and UIDadmn2. This is accomplished for UIDadmn1 by 
joining the strings of the unique identifier columns of 'ID_0' and 'ID_1'. For example if ID_0 is 1 and ID_1 is 12, then UIDadmn1 
will be 112. UIDadmn2 codes will be the same methodology, but by combining 'ID_0', 'ID_1', and 'ID_2'. 

'''

from __future__ import division
import time
import os
import pandas as pd
import numpy as np

# start time
start_time = time.time()

# set path to folder containing the csv output of shapefile
filepath = [r'F:\TimData\Admin\NewGadm' + '\\']

def addadmncodes():
    """Function to concatenate two or three columns of data together. First converting from integer to string
    """
    try:
        # read csv file of gadm shapefile
        df = pd.read_csv(filepath[0] + 'NewGadm.csv')
        # specify columns to work on and convert to string
        col1 = df['ID_0'].apply(str)
        col2 = df['ID_1'].apply(str)
        col3 = df['ID_2'].apply(str)
        
        # First concatenate admn 0 codes and admn 1 codes
        df["UIDadmn1"] = col1 + col2
        # Now concatenate admn0, admn1, and admn2 codes
        df["UIDadmn2"] = col1 + col2 + col3
        # write output to csv file
        df.to_csv(filepath[0] + 'NewGADM_admncodes2.csv') 
    except IOError:
        print "Encountered error, check file location and file"

def main():
    """function to implement function
    """
    addadmncodes()

if __name__ == "__main__":
    main()


# print time script finished  
print time.time() - start_time, "seconds, finished" 
