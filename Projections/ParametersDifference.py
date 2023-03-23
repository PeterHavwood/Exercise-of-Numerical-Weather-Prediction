# m,l-latitude relations in different projections

import os
import numpy as np
import matplotlib.pyplot as plt
from math import exp, pow, log, sqrt, cos, sin, asin, degrees, pi, e, inf

EarthRadius = 6.371e6
latitude = range(0, 91, 1)

m_plane = np.zeros(91)
m_lambert = np.zeros(91)
m_mercator = np.zeros(91)
l_plane = np.zeros(91)
l_lambert = np.zeros(91)
l_mercator = np.zeros(91)

for lat in range(0, 91, 1):
    phi = lat/180.0 * pi

    m_plane[lat] = (1 + sin(pi/3)) / (1 + sin(phi))
    l_plane[lat] = EarthRadius * (1 + sin(pi/3)) * cos(phi) / (1 + sin(phi)) 

    K_lambert = 0.71557
    A = cos(pi/3) * pow((1 + sin(pi/3))/cos(pi/3), K_lambert) 
    m_lambert[lat] = A / (cos(phi) * pow((1 + sin(phi))/cos(phi), K_lambert) )
    l_lambert[lat] = EarthRadius * A * pow(cos(phi)/(1 + sin(phi)), K_lambert) / K_lambert

    phi_225 = 22.5/180 * pi
    if(lat == 90): 
        m_mercator[lat] = inf
        l_mercator[lat] = inf
        break
    m_mercator[lat] = cos(phi_225) / cos(phi)
    l_mercator[lat] = EarthRadius * cos(phi_225) * log(cos(phi) / (1-sin(phi)), e)

figPath = 'Figures'
if not os.path.exists(figPath):
    os.makedirs(figPath)

# Plot the m in different projections
fig1, ax1 = plt.subplots()

ax1.plot(latitude, m_plane, label = "Plane")
ax1.plot(latitude, m_lambert, label = "Lambert")
ax1.plot(latitude, m_mercator, label = "Mercator")

ax1.set_title('m-latitude Relations in Different Projections')
ax1.legend()
ax1.set_xlabel("latitude")
ax1.set_xbound(0, 90)
ax1.set_ybound(0.75, 2)
ax1.grid(True)

fig1.savefig(os.path.join(figPath,'m.jpg'))

# Plot the l in different projections
fig2, ax2 = plt.subplots()

ax2.plot(latitude, l_plane*1e-7, label = "Plane")
ax2.plot(latitude, l_lambert*1e-7, label = "Lambert")
ax2.plot(latitude, l_mercator*1e-7, label = "Mercator")

ax2.set_title('l-latitude Relations in Different Projections')
ax2.legend()
ax2.set_xlabel("latitude")
ax2.set_ylabel("l ($10^7m/s$)")
ax2.set_xbound(0, 90)
ax2.set_ybound(0, 2)
ax2.grid(True)

fig2.savefig(os.path.join(figPath,'l.jpg'))