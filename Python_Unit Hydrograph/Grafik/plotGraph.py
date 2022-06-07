
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rd_csv as rd

# name of file to read data and save output file
filename= 'UH.csv'# filename without csv extension
figurename = 'UH.png'
rd.read_csv(filename)

print('oiii',rd.time[0], rd.P[0], rd.Q[0])

# Plot Data vs ANNOutput (time series) and Data vs ANNOutput (Correlation)
#mpl.rc('font', family='serif') 
#mpl.rc('font', serif='Helvetica Neue')
#mpl.rc('text', usetex='true')
#mpl.rcParams.update({'font.size': 14})

from scipy.interpolate import make_interp_spline, BSpline

# 300 represents number of points to make between min and max of time
time_new = np.linspace(rd.time.min(), rd.time.max(), 300) 
Q_spline = make_interp_spline(rd.time, rd.Q, k=3)  # type: BSpline
Q_new = Q_spline(time_new)

# Draw Graph
fig, ax = plt.subplots(2, 1, sharex='col', sharey='row')
ax[0].bar(rd.time, rd.P, label='Hujan Satuan (1 cm)')
ax[0].set_title('')
ax[0].set_ylabel('Hujan (cm)')
ax[0].invert_yaxis()

ax[1].plot(time_new, Q_new, 'b-', markersize=4, label='Hidrograf Satuan')
ax[1].set_xlabel('Time (x 1/2 jam)')
ax[1].set_ylabel('Hidrograf Satuan (m^3/detik)')
ax[1].legend(loc='upper right', shadow=False, frameon=False)

fig.savefig(figurename)
plt.show()
