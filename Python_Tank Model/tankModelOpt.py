import rd_csv as rd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

filename = 'rrtestDat.csv'
figurename = 'rainfallRunoff.png'
rd.read_csv(filename)
# column name become variable name rd.Rain, rd.Runoff, rd.ET

# name of file to save optimized parameters
paramFilename = 'optParam.csv'


def Perc(a, H1):
    Ya = a * H1
    return Ya

def subRunoff(b, H1, Hb):
    Yb = b * (H1 - Hb)
    if (Yb<0):
        Yb = 0
    return Yb

def Runoff(c, H1, Hc):
    Yc = c * (H1 - Hc)
    if (Yc<0):
        Yc = 0
    return Yc

def gwFlow(d, H2):
    Yd = d * H2
    return Yd

def Tank(H, t, a, b, c, d, Hb, Hc, Rain, ET):
    H1 = H[0]
    H2 = H[1]
    Ya = Perc(a, H1)
    Yb = subRunoff(b, H1, Hb)
    Yc = Runoff(c, H1, Hc)
    Yd = gwFlow(d, H2)
    dH1dt = Rain - (ET + Ya + Yb + Yc)
    dH2dt = Ya - Yd
    return np.array([dH1dt, dH2dt])

#initial value
a = 0.17 #0.00003
b = 0.000002 #0.0003
c = 0.000106 #0.0003
d = 0.02 #0.0002
Hb= 1.99
Hc= 10.72
H10 = 0
H20 = 0

Param = (a, b, c, d, Hb, Hc, H10, H20)
H0 = np.array([H10, H20]) # initial condition of H1, H2
H1 = np.zeros(len(rd.Rain)); H1[0] = H0[0]
H2 = np.zeros(len(rd.Rain)); H2[0] = H0[1]

# time array definition in days
t = np.linspace(1, len(rd.Rain), len(rd.Rain))

def Discharge(c, H1, Hc):
    Yc = c * (H1 - Hc)
    Yc[Yc<=0] = 0
    return Yc

def SSE_Discharge(Param):
    a, b, c, d, Hb, Hc, H10, H20 = Param
    H0 = np.array([H10, H20])
    for i in range(1, len(t)):
        # span for next time step
        tspan = [t[i-1], t[i]]
        # solve for next step
        # the use of tspan make H contains two rows, 2 column each
        H, infodict = odeint(Tank, H0, tspan, args=(a, b, c, d, Hb, Hc, rd.Rain[i], rd.ET[i]), full_output=True)
        infodict['message']
        # store solution for plotting
        H1[i] = H[1][0] # use second row H[1] for newer value, first column [0]
        H2[i] = H[1][1] # use second row H[1] for newer value, second column [1]
        # next initial condition
        H0 = H[1] # use second row H[1] for newer value, both columns
    Yc = Discharge(c, H1, Hc)
    SSE = np.sum((Yc - rd.Runoff)**2)
    return SSE

Debit_init = Discharge(c, H1, Hc)

# Parameter optimation of a, b, c, d, Hb, Hc, H10, H20
from scipy.optimize import minimize # Optimization
cons = ({'type': 'ineq', 'fun': lambda Param:  Param}) # all values inside Param>0
result = minimize(SSE_Discharge, Param, method='BFGS', constraints=cons, options={'disp':True})
opt_vals = result.x ; a, b, c, d, Hb, Hc, H10, H20 = opt_vals
print(a, b, c, d, Hb, Hc, H10, H20)
Debit = Discharge(c, H1, Hc)

# Save to file
# Procedure to save optimal parameters
with open(paramFilename, 'a') as f:
    optParam = str(a)+','+str(b)+','+str(c)+','+str(d)+','+str(Hb)+','+str(Hc)+','+str(H10)+','+str(H20)
    f.seek(0)                                                       # find firt line
    f.truncate()                                                    # delete all data below
    f.write('a, b, c, d, Hb, Hc, H10, H20'+'\n')
    f.write(optParam)

# Draw Graph
fig, ax = plt.subplots(2, 1, sharex='col', sharey='row')
ax[0].bar(t, rd.Rain)#, 'b--', markersize=4, label='Rainfall (data)')
ax[0].set_title('Tank Model : Rainfall-Runoff')
ax[0].set_ylabel('Rainfall (mm)')
ax[0].invert_yaxis()

ax[1].plot(t, rd.Runoff, 'ro-', markersize=4, label='Runoff (data)')
ax[1].plot(t, Debit, 'b-', markersize=4, label='Runoff (model)')
ax[1].plot(t, Debit_init, 'b--', markersize=4, label='Runoff initial (model)')
ax[1].set_xlabel('Time (hours)')
ax[1].set_ylabel('Runoff (m3/s)')
ax[1].legend(loc='upper right', shadow=False, frameon=False)

fig.savefig(figurename)
plt.show()



