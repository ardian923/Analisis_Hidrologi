#writen by Dr. Ardiansyah (ardi.plj@gmail.com) in 2022 for Hydrology Analysis
#don't delete this first two lines

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rd_csv as rd

import unitHydrograph as uh

# name of file to read data and save output file
fileName1= 'Discharge.csv'# filename without csv extension
figName1 = 'Discharge.png'
rd.read_csv(fileName1) #column name become variable name : P, Q

# prepare file for storing result
fileName2 = 'unitHydr.csv'
figName2  = 'unitHydr.png'

N = len(rd.Q)
M = np.count_nonzero(rd.P)
U = N-M+1

# calculate unit hydrograph from data
UH = uh.unitHydrograph(N, M, rd.P, rd.Q)
uhTime = rd.time[:U]
uhP = np.zeros(uhTime.size)
uhP[0] = 1
print ('Hidrograf Satuan (Unit Hydrograph) : ', UH)

# Save to file
# Procedure to save unit hydrograph to file
with open(fileName2, 'a') as f:
    f.seek(0)                                                       # find firt line
    f.truncate()                                                    # delete all data below
    f.write('uhTime, uhP, UH \n')
    for i in range(U):
        wrtUH = str(uhTime[i])+','+str(uhP[i])+','+str(UH[i])
        f.write(wrtUH+'\n')

# plot graph of Discharge Data
from scipy.interpolate import make_interp_spline, BSpline

time_new = np.linspace(rd.time.min(), rd.time.max(), 300) 
Q_spl = make_interp_spline(rd.time, rd.Q, k=3)  # type: BSpline
Q_new = Q_spl(time_new)

# Draw Graph
fig1, ax1 = plt.subplots(2, 1, sharex='col', sharey='row')
ax1[0].bar(rd.time, rd.P, label='Data Hujan (cm)')
ax1[0].set_title('')
ax1[0].set_ylabel('Hujan (cm)')
ax1[0].invert_yaxis()

ax1[1].plot(time_new, Q_new, 'b-', markersize=4, label='Data Debit')
ax1[1].set_xlabel('Time (x 1/2 jam)')
ax1[1].set_ylabel('Debit (m^3/detik)')
ax1[1].legend(loc='upper right', shadow=False, frameon=False)

fig1.savefig(figName1)

# plot graph of the UH
uhTime_new = np.linspace(uhTime.min(), uhTime.max(), 300) # 300 represents number of points to make between min and max of time
UH_spl = make_interp_spline(uhTime, UH, k=3)  # type: BSpline
UH_new = UH_spl(uhTime_new)

fig2, ax2 = plt.subplots(2, 1, sharex='col', sharey='row')
ax2[0].bar(uhTime, uhP, label='Hujan Satuan (1 cm)')
ax2[0].set_title('')
ax2[0].set_ylabel('Hujan (cm)')
ax2[0].set_ylim([0, 10])
ax2[0].invert_yaxis()

ax2[1].plot(uhTime_new, UH_new, 'b-', markersize=4, label='Hidrograf Satuan')
ax2[1].set_xlabel('Time (x 1/2 jam)')
ax2[1].set_ylabel('Hidrograf Satuan (m^3/detik)')
ax2[1].legend(loc='upper right', shadow=False, frameon=False)

fig2.savefig(figName2)


plt.show()
