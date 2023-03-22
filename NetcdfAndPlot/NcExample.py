# There are 4 Netcdf files of 4 latitudes, which contains the wind, height and other informations
# We need to calculate the advection term, coriolis term and pressure term of each point in time
import math
import os

import netCDF4 as nc
import numpy as np

import matplotlib.pyplot as plt

file = ['ELat.198101-201012.clt.nc','lLat.198101-201012.clt.nc','mLat.198101-201012.clt.nc','hLat.198101-201012.clt.nc']

# Read the latitude, pressure, time(in month)
dataForVar = nc.Dataset(file[0])
lon = dataForVar.variables['lon'][:]
lev = dataForVar.variables['lev'][:]
time = dataForVar.variables['time'][:]

# Set the longtitude
lat = [0, 15, 45, 75]
# The ln value of different pressures
lnLev = np.zeros(len(lev))
for i in range(0,len(lev)):
    lnLev[i] = math.log(lev[i],math.e)

# init A = A(time, lev, lat, lon)
advection = np.zeros([len(time), len(lev), len(lat), len(lon)])
coriolis = np.zeros([len(time), len(lev), len(lat), len(lon)])
pgf = np.zeros([len(time), len(lev), len(lat), len(lon)])

# ticks for plot
monthInHour = [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016]
monthName = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

LatInDegree = [0, 60, 120, 180, 240, 300, 360]
latName = ['0','60E','120E','180E','120W','60W','0']

lnLevTick = [lnLev[0],lnLev[2],lnLev[5],lnLev[8],lnLev[11],lnLev[15]]
levTick = [lev[0],lev[2],lev[5],lev[8],lev[11],lev[15]]

for latNum in range(0,len(lat)):
    # Read nc file
    data = nc.Dataset(file[latNum])

    # Set constants: distance bettwen 2 points, f the coriolis parmeter, g
    d = 6.38*1e6*math.radians(2.5)*math.cos(math.radians(lat[latNum]))
    f = 2*7.29*1e-5*math.sin(math.radians(lat[latNum]))
    g = 9.8

    # for every pressure in every month
    for timeNum in range(0,len(time)):
        for levNum in range(0,len(lev)):
            
            u = data.variables['uwnd'][timeNum,levNum,:,:]
            v = data.variables['vwnd'][timeNum,levNum,:,:]
            h = data.variables['hgt'][timeNum,levNum,:,:]
            
            advection[timeNum,levNum,latNum,0] = u[0,0] * (u[0,1]-u[0,143])/(2*d)
            advection[timeNum,levNum,latNum,143] = u[0,142] * (u[0,0]-u[0,142])/(2*d)
            for lonNum in range(1,len(lon)-1):
                advection[timeNum,levNum,latNum,lonNum] = u[0,lonNum] * (u[0,lonNum+1]-u[0,lonNum-1])/(2*d)
            
            coriolis[timeNum,levNum,latNum,:] = f * v
            
            pgf[timeNum,levNum,latNum,0] = -g * (h[0,1]-h[0,143])/(2*d)
            pgf[timeNum,levNum,latNum,142] = -g * (h[0,0]-h[0,142])/(2*d)
            for lonNum in range(1,len(lon)-1):
                pgf[timeNum,levNum,latNum,lonNum] = -g * (h[0,lonNum+1]-h[0,lonNum-1])/(2*d)

# Now we can plot differnt figures

# Plot the Contour figure of adveciton term in month-longitude
for latNum in range(0,len(lat)):
    for levNum in range(0,len(lev)):

        fig, ax = plt.subplots()
        # Set the level for contourf
        min = np.min(1e5*advection[:,levNum,latNum,:])
        max = np.max(1e5*advection[:,levNum,latNum,:])
        level = np.arange(min,max,(max-min)/10)
        # Use contourf to plot. The parameters are: x, y, z，the contour line of z to plot, color
        cf = ax.contourf(lon, time, 1e5*advection[:,levNum,latNum,:], levels = level, cmap='rainbow', extend = 'both')
        # The bar of z-level
        cb = fig.colorbar(cf)
        # Set titel and ticks
        ax.set_title('month-longitude seciton of advection term @'+str(lev[levNum])+'hPa '+str(lat[latNum])+'°N')
        cb.set_label('unit: $10^{-5} m/s^2$')
        ax.set_xticks(LatInDegree,latName)
        ax.set_yticks(monthInHour,monthName)
        # Save the figure
        figPath = 'month-lon adv'
        if not os.path.exists(figPath):
            os.makedirs(figPath)
        fig.savefig(os.path.join(figPath,str(lev[levNum])+'hPa-'+str(lat[latNum])+'.jpg'))

# Plot the average of 3 terms of different longitudes
for latNum in range(0,len(lat)):
    for levNum in range(0,len(lev)):

        timeMeanAdvection = 1e5*np.average(advection,0)
        timeMeanCoriolis = 1e5*np.average(coriolis,0)
        timeMeanPgf = 1e5*np.average(pgf,0)

        fig, ax = plt.subplots()
        # add 3 lines of the 3 terms
        ax.plot(lon, timeMeanAdvection[levNum,latNum,:], label='advection term')
        ax.plot(lon, timeMeanCoriolis[levNum,latNum,:], label='coriolis term')
        ax.plot(lon, timeMeanPgf[levNum,latNum,:], label='pressure term')
        # Set titel and labels
        ax.set_title('12month averaged term-lontitude @'+str(lev[levNum])+'hPa '+str(lat[latNum])+'°N')
        ax.set_xticks(LatInDegree,latName)
        ax.set_xbound(0,360)
        ax.set_ylabel('$10^{-5}m/s^2$')
        ax.legend()
        # Save the figure
        figPath = 'term-lon'
        if not os.path.exists(figPath):
            os.makedirs(figPath)
        fig.savefig(os.path.join(figPath,str(lev[levNum])+'hPa-'+str(lat[latNum])+'°.jpg'))