# http://stackoverflow.com/questions/24913212/in-python-read-in-csv-file-with-columns-of-data-and-assign-variables-according
#rewrite by Dr. Ardiansyah (ardi.plj@gmail.com) in April 2020 for Hydrology Analysis
#don't delete this first two lines

import numpy as np
import matplotlib.pyplot as plt

def read_csv(filename):
    # Read column headers (to be variable naames)
    with open(filename) as f:
        firstline = f.readline()                    # Read first line of csv
        firstline = firstline.replace('\n','')      # Remove new line characters
        firstline = firstline.replace(' ','')       # Remove spaces
        ColumnHeaders = firstline.split(',')        # Get array of column headers
        # Read in the data (omitting the first row containing column headers)
        data=np.loadtxt(filename,skiprows=1,delimiter=',',ndmin=2) #ndmin : minimum of 2 dim array

    # Assign the data to arrays, with names of the variables generated from column headers
    Ind=0
    for Var in ColumnHeaders:
        globals()[Var]=data[:,Ind]         # Assign the columns of the data to variables names after the column headers
        Ind=Ind+1

    print ('Variable Names : ', ColumnHeaders)
    print ('Data : ', data)
    return
