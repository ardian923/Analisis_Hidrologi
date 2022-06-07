#! /usr/bin/env python
## Water Uptake Simulation
## Developed for lecture, by Ardiansyah (UNSOED), http://ardiansyah.net

import numpy as np  ##numerical python library
import matplotlib.pyplot as plt ##plotting library
import scipy as sc  ##scientific python library
#import math as mth  ##matemathical operation library
import time

# Input  
m   = 13    # Number of soil layer from 0 to 12
ETp = 6     # Evapotranspiration (mm/day), asumsi konstan untuk kasus ini
rsto0 = 100 # Monteith 1981
sp  = 10
pc  = -3400 # kPa, critical leaf water potential (950 kPa, http://www.sciencedirect.com/science/article/pii/030438009090046J)
pl  = -1500 # kPa, initial leaf water potential
bv = 7.9    # Soi b value, Campbell
LAI = 4     # Leaf Area Index
day_end = 2 # Number of days simulation run

depth = 50           # depth of soil root zone is 50 cm
z = np.zeros(m)      # reserve spae for z array
p = np.zeros(m)      # reserve space for soil water potential
p[:] = -100          # assign all array with similar value
pe = -3.4            # air entry potential , kPa
ksat = 0.000025      # Saturated ydraulic conductivity, kg s/m3
dz  = depth/(m-1)    # depth of soil layer (discretization)
## Discrete soil into several layers
z[0] = 0
for i in range(1, m):
    z[i] = z[i-1] + dz

def soilHydraulicConductivity(p, pe):
    n = 2 + 3/bv
    Kh = ksat * np.power((pe/p), n)
    return Kh

def partitionETp(hour, ETp):                                        ## partitioning Potential EvapoTranspiration (daily to hourly)
    ETp_hour = 2.3*ETp*(0.05+(np.sin(0.175*7.5*hour/(-np.pi/180)))+4)/86400      ## ETp pot Evapotranspiration rate, mm/day
    Ep    = np.exp(-0.29*LAI)*ETp_hour                             ## Maruyama et.al. (2007), tau_c = exp(-0.29*LAI)
    Tp    = ETp_hour-Ep                                             ## Eq 12.30 (Cambpel Soil Phys with BASIC)
    ## Rain or Irrig can be added by setting U[0] to desired flux density
    return Tp

def rcanopy(rsto0, LAI, pl, pc):
    xp    = np.power((pl/pc),sp)    
    rsto = rsto0*(1+xp)                        ## when leaf water potential decreases below critical}
    rl   = rsto/LAI
    return rl

def rootDensity(z):
    Li = np.zeros(m)
    Li[0] = 0
    for i in range(1, m):
        Li[i] = 523.62* np.power(z[i], - 2.24)
        # print (Li[i])
    return Li

## water flow algorithm needed to asses soil water potential 

def rootInitialization(z):
    rw = 2.5e10
    d1 = 0.001                         ## Diameter akar, perlu untuk menghitung luas akar
    n = np.zeros(m); n[:] = 2 + 3/bv
    Li = np.zeros(m); rr = np.zeros(m); bz = np.zeros(m)
    Li = rootDensity(z) 	       ## Root density function of depth (1/m2)	
    Li = 1000 * Li
    for i in range(1, m-1):
        if (Li[i]>0):
            rr[i] = 2*rw/(Li[i]*(z[i+1]-z[i-1]))
            bz[i] = (1-n[i])*np.log(np.pi*np.power(d1,2)*Li[i])/(2*np.pi*Li[i]*(z[i+1]-z[i]))
        else:
            rr[i] = 1e+20
            bz[i] = 0
    return rr, bz

def waterUptake(rr, bz, Tp, pl):
    ps = 0; rs_ = 0; xp = 0
    Kh = np.zeros(m); rs = np.zeros(m)
    for i in range(m):
        Kh[i] = soilHydraulicConductivity(p[i], pe)
        rs[i] = bz[i]/Kh[i]
        ps = ps + p[i]/(rr[i]+rs[i])
        rs_= rs_ + 1/(rs[i] + rr[i])

    ps = ps/rs_				## 11.18 (Cambpel Soil Phys with BASIC)
    rs_= 1/rs_				## total root, soil, xylem resistance

    if (pl>ps):
        rl = rcanopy(rsto0, LAI, pl, pc)
        pl = ps - Tp*(rl+rs_)            ## no water stress, transp potential = water uptake
  
    rl = rcanopy(rsto0, LAI, pl, pc)
    F  = ps-pl-Tp*(rl+rs_)/(1+xp)     ## pl = ps - (Tp/(1+xp))*(rl+rs_), F = 0
    while (F>10):                       ## repeat to correct pl, until F < 10
        xp    = np.power((pl/pc),sp)    
        rl    = rcanopy(rsto0, LAI, pl, pc)
        dFdpl = Tp*(rl+rs_) * sp * xp/ (pl*sqr((1+xp)))-1 ## dF/dpl, derivative of F over pl
        F     = ps-pl-Tp*(rl+rs_)/(1+xp) ## pl = ps - (Tp/(1+xp))*(rl+rs_), F = 0
        pl    = pl- (F/dFdpl)           ## correct pl value

    Tr = Tp/(1 + xp)			## Tr is actual transpiration

    ## calculate water uptake in each soil layer
    U = np.zeros(m); U[:] = 0
    for i in range(m):
        ## water uptake = (psoil - pleaf)/(rroot + r soil) - (Tr * rleaf)/(rroot + rsoil)
        U[i] = (p[i]-pl-rl*Tr)/(rr[i]+rs[i])                                   
    return Tr, U

def main():
    day  = 0
    hour = 0
    hrTime = []
    TrTime = []   
    while (day<=day_end):
        Tp = partitionETp(hour, ETp)
        rr, bz = rootInitialization(z)
        Tr, U  = waterUptake(rr, bz, Tp, pl)
        print (hour, Tr)
        hrTime.append(hour)
        TrTime.append(Tr)

        hour = hour + 1
        if np.mod(hour, 24) != 0:
            day = day
        else:
            day = day + 1

    fig, ax = plt.subplots(1, 1, sharex='col', sharey='row')
    ax.plot(hrTime, TrTime, label='')
    ax.set_title('Hourly Transpiration')
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Transpiration (mm/s)')
    #ax.set_ylim([0, 10])
    #ax.invert_yaxis()

    plt.show()
    return


if __name__ == '__main__': # run water uptake
    main()

## EOF (End of File)
