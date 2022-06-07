# pyDoubleLayerEB : Double Layer Model for Energy Balance in Bare and Vegetated Surface

\pagebreak

Water Flow in Soil due to Infiltration or Evaporation
-----------------------------------------------------
Water flow in soil when there is gradient in soil matric pressure. The gradient could occur through infiltration (water in soil surface) or evaporation flux (vapor movement in soil surface)

**Liquid Flux :**

$q_l = k_h \frac{\partial \psi}{\partial z} + 1$

where :

$k_h = k_s e^{-{a_1}  ((1- (\frac{\theta}{\theta_s})^{b_1})^{c_1})}$
$a_1$ = 40.3 ;
$b_1$ = 0.672 ; 
$c_1$ = 3.31. 
The unit of  $k_h$ is depends on the unit of $k_s$

Water retention curve is given by equation :
$\theta = \frac{a}{(1+(b \psi)^c)^d}  + e (1- (\frac{log(\psi + 1)}{f})$, 
where $\psi$ is matric potential in $mH_2O$, 

$a$ = 0.343; 
$b$ = 0.04133; 
$c$ = 5.603; 
$d$ = 0.8215; 
$e$ = 0.08624; 
$f$ = 14.37. 
Water capacity is calculated as  $\frac{d \theta}{d \psi}$


**Vapor Flux :**

$q_v = k_v \frac{\partial \psi}{\partial z} + k_{vT} \frac{\partial T}{\partial z}; (kg.m^{-2}s^{-1})$ --> if divided by $\rho_w$ ($kg.m^{-3}$), resulting flux in $m.s^{-1}$


where :

$k_v = 0.66 . \phi . D_v . \rho_v . \frac{h_r M_w}{R T}$; ($kg.s.m^{-3}$)

$k_{vT} = 0.66 . \phi . D_v . \frac{d \rho'_v}{d T} . \eta . h_r$; ($kg.s^{-1}.m^{-1}.K^{-1}$)

$h_r$ is soil relative humidity

$h_r = e^{ \frac{(M_w \psi)}{R  (T + 273)}}$

$\rho'_v = (\frac{1}{T_k})  e^{31.3716 - \frac{6014.79}{T_k} - 0.00792495 . T_k}$ ($g.m^{-3}$) - - -> if divided by 1000, resulting $kg.m^{-3}$; 

$\rho_v = h_r . \rho'_v$

$D_v$ = vapor difussivity (0.000024 $m^2.s^{-1}$); 
$R$ = gas constant (8.3143 $J.mole^{-1}.K^{-1}$); 
$M_w$ = mass of a mole water (0.018 $kg.mole^{-1}$); 
$T$ = temperature (Kelvin); 
$\phi$ = air filled porosity

```python
    kvi  = 0.66 * phi_i * Dv * (Mw / (R * (Ti[i] + 273))) * rhov_i  ## Dv, Mw inputted in spreedsheet
    kvTi = 0.66 * phi_i * Dv * drhov_sati * eta * hbar_i
    kvn  = 0.66 * phi_n * Dv * (Mw / (R * (Tn[i] + 273))) * rhov_n
    kvTn = 0.66 * phi_n * Dv * drhov_satn * eta * hbar_n
```
	


\pagebreak


Heat Flow in Soil
-----------------
Heat flow in soil occures due to the existance of heat source. Soil surface explosed to solar radiation is the heat source.

\pagebreak


Single Layer Energy Balance
---------------------------
Single layer energy balance assumes soil and plant are 1-layer that release vapor to air. Both evaporation (E) and transpiration (T) calculated as ET. Penman-Monteith equation is used to draw the relation.

```python
def PenmanMonteith_ETo(u, Ta, Twb, ha, Rn, Go):
    lamda = LatentHeatVaporize(Ta)
    e_sat, de_sat = SVP(Ta)   
    e_act = AVP(Ta, Twb, alt)
    VPD = e_sat - e_act   
    Pa = AtmPressure(alt)
    gamma = PsycConstant(Pa, Ta)
    rho_a = AtmDensity(Pa, Ta)     
    u2 = u * (4.87)/(np.log(67.8*ha - 5.42))
    raa = 208./u2 				   ## aerodynamic resistance (s/m)
    rca = 30 ## daytime = 50 (short plant <0.5 m), 30 (tall plant > 0.5), nighttime = 200 (s/m)
    PenmanMonteith_ETo = (1/lamda) * (de_sat * (Rn - Go) +  (VPD * rho_a * Cp)/raa)/(de_sat + gamma * (1+(rca/raa)))
    return PenmanMonteith_ETo
## end Penman-Monteith ET calculation
```

Penman-Monteith equation take soil and canopy as isothermal. First term of the eqiauation considering soil surface that requires Net Radiation ($R_n$) and Ground Heat Flux ($G_o$). Second term of equation is about vapor transport from canopy that depends on canppy resistance ($rca$) and aerodynamic resistance ($raa$)

\pagebreak

Double Layer Energy Balance
---------------------------

Double Layer Evapotranspiration Model Describe as : 

![alt text][double_layer]

[double_layer]: 0_double_layer.png "Double Layer Model"

\pagebreak


```python

```
