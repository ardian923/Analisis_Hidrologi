#writen by Dr. Ardiansyah (ardi.plj@gmail.com) in 2022 for Hydrology Analysis
#don't delete this first two lines

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rd_csv as rd

import unitHydrograph as uh

# name of file to read data and save output file
fileName1 = 'unitHydr.csv'
figName1  = 'unitHydr.png'
rd.read_csv(fileName1) #column name become variable name : P, Q, UH

# prepare file for storing result
fileName2= 'resultDischarge.csv'# filename without csv extension
figName2 = 'resultDischarge.png'

# input rainfall data for P
P = np.array([5, 25, 10, 3, 30, 50])

U = len(rd.UH)
M = len(P)
N = U+M-1
zP = np.zeros(N-M)
print ('zP oiii', zP)
rP = np.concatenate((P, zP), axis=None)
print ('rP oiii', rP)

# calculate runoff discharge hydrograph from data
Q = uh.runoffDischarge(N, M, P, rd.UH)
time = np.array(range(1,N+1))
print ('Hidrograf Debit : ', Q)

# Save to file
# Procedure to save unit hydrograph to file
with open(fileName2, 'a') as f:
    f.seek(0)                                                       # find firt line
    f.truncate()                                                    # delete all data below
    f.write('time, P, Q \n')
    for i in range(N):
        wrtQ = str(time[i])+','+str(rP[i])+','+str(Q[i])
        f.write(wrtQ+'\n')

from scipy.interpolate import make_interp_spline, BSpline
# plot graph of the UH
uhTime_new = np.linspace(rd.uhTime.min(), rd.uhTime.max(), 300) # 300 represents number of points between min and max
UH_spl = make_interp_spline(rd.uhTime, rd.UH, k=3)  # type: BSpline
UH_new = UH_spl(uhTime_new)

fig1, ax1 = plt.subplots(2, 1, sharex='col', sharey='row')
ax1[0].bar(rd.uhTime, rd.uhP, label='Hujan Satuan (1 cm)')
ax1[0].set_title('')
ax1[0].set_ylabel('Hujan (cm)')
ax1[0].set_ylim([0, 10])
ax1[0].invert_yaxis()

ax1[1].plot(uhTime_new, UH_new, 'b-', markersize=4, label='Hidrograf Satuan')
ax1[1].set_xlabel('Time (x 1/2 jam)')
ax1[1].set_ylabel('Hidrograf Satuan (m^3/detik)')
ax1[1].legend(loc='upper right', shadow=False, frameon=False)

fig1.savefig(figName1)

# plot graph of Discharge Data
time_new = np.linspace(time.min(), time.max(), 300) 
Q_spl = make_interp_spline(time, Q, k=3)  # type: BSpline
Q_new = Q_spl(time_new)

# Draw Graph
fig2, ax2 = plt.subplots(2, 1, sharex='col', sharey='row')
ax2[0].bar(time, rP, label='Data Hujan (cm)')
ax2[0].set_title('')
ax2[0].set_ylabel('Hujan (cm)')
ax2[0].invert_yaxis()

ax2[1].plot(time_new, Q_new, 'b-', markersize=4, label='Hasil Debit')
ax2[1].set_xlabel('Time (x 1/2 jam)')
ax2[1].set_ylabel('Debit (m^3/detik)')
ax2[1].legend(loc='upper right', shadow=False, frameon=False)

fig1.savefig(figName2)



plt.show()
