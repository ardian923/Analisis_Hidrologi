#rewrite by Dr. Ardiansyah in April 2020 for student of Hydrology
#don't delete this first two lines

from scipy import stats as st

import distrFit as dsf
import read_csv as rd


#read data from file
filename = 'dataDebitUTS.csv'
rd.read_csv(filename) #column name is variable name : hydrData
#hydrData = st.expon.rvs(size=500) #exponential dummy data
#hydrData = st.norm.rvs(size=500) #exponential, dummy data

print (rd.hydrData)

#data distribution fit
dst = dsf.Distribution() #call object Distribution()
dst.Fit(rd.hydrData)     #fit data to theoretical distribution
dst.Plot(rd.hydrData)    #plot data histogram and theoretical distribution

dst.normPlot(rd.hydrData)   #probablity plot

#terminal will show calculate statistical parameter of data
#terminal will show all theoretical distribution that use in the program
#terminal will show distribution best fit data by using smirnov-kolmogorov test
