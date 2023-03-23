# This program is to output the latitude and other parameters of a certain point(i,j)
# The plane of the projection cuts off the earth at 60°N
# The original poiont of the rectangular plane coordinate system is the pole

from math import pow, sqrt, cos, sin, asin, degrees, pi

EarthRadius = 6.371e6
EarthRotation = 7.292e-5
L_eq = EarthRadius * (1 + sin(pi/3))
d = 5e5     # the unit lenth of the axes

# the point(i,j)
i = -4
j = 8

# formulas to cauculate
L_ij = sqrt(pow(i*d,2) + pow(j*d,2))
A = pow(L_ij / L_eq,2)
phi_ij = asin((1 - A) / (1 + A))

latitude_ij = degrees(phi_ij)
m_ij = (1 + sin(pi/3)) / (1 + sin(phi_ij))
f_ij = 2 * EarthRotation * sin(phi_ij)

print("The latitude of point is: " + str(latitude_ij) + "°N.")
print("The m of point is: " + str(m_ij) + ".")
print("The f of point is: " + str(f_ij) + ".")