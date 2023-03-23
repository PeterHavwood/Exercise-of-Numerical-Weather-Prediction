# This program is to output the latitude and other parameters of a certain point(i,j)
# The plane of the projection cuts off the earth at 22.5°N and 22.5°S
# The original poiont of the rectangular plane coordinate system is the pole

from math import exp, pow, sqrt, cos, sin, asin, degrees, pi

EarthRadius = 6.371e6
EarthRotation = 7.292e-5
phi_0 = 22.5/180 * pi
d = 2e5     # the unit lenth of the axes

# the point(*,j)
j = 3

# formulas to cauculate
L_ij = j * d
A = exp(2 * L_ij / (EarthRadius * cos(phi_0)))
phi_ij = asin((A - 1) / (A + 1))

latitude_ij = degrees(phi_ij)
m_ij = cos(phi_0) / cos(phi_ij)
f_ij = 2 * EarthRotation * sin(phi_ij)

print("The latitude of point is: " + str(latitude_ij) + "°N.")
print("The m of point is: " + str(m_ij) + ".")
print("The f of point is: " + str(f_ij) + ".")
