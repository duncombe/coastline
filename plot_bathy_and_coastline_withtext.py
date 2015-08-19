# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:18:20 2015
Read in a comma delimited file of lon, lat and bathy and plot
@author: SeaLaptop
"""
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.path import Path
import matplotlib.patches as patches

# Boundaries for plotting
lonmin = 18.2                 # Longitude minimum
lonmax = 19.0                 # longitude maximum
latmin = -34.6                # latitude minimum
latmax = -33.8                # latitude maximum
# Extremities in the Bathy file
Blonmin = 15
Blonmax = 30
Blatmin = -43
Blatmax = -33


## Reading the Bathy
inputfile = 'bathy_agulhas_2.dat'                   # The name of the bathymetry input file
print('Opening bathy input file:',time.asctime())
INPUT = open(inputfile,'r')                         # Opens the file with read-only priviledges and creates a handle to the file called 'INPUT'
lon = []                                            # Prepares an empty list to store longitude values
lat = []                    
bathy = []
# this for loop will store the bathy, longitude and latitude as a list each
for line in INPUT:                                  # Each iteration reads a line from the INPUT file and stores it as a string called 'line'
    line.strip()                                    # Removes the hidden newline character from the line
    if line[0] is not '*':                          
        lineS = line.split(',')                     # Split the string into a list of elements, using the comma as a delimiter
        lon.append(float(lineS[0]))                 # Take the first element, convert it to a float, and then append that number to the end of the longitude list
        lat.append(float(lineS[1]))
        bathy.append(float(lineS[2]))
        # the lists contain 2 million elements each after this loop ends

nlons = (Blonmax-Blonmin) * 60 * 2         # number of longitude grid points in the bathy dataset
nlats = (Blatmax-Blatmin) * 60 * 2         # 33 deg S to 43 deg S ..... 10 degrees of latitude, 60 miniutes per degree, 2- 30sec intervals per minute
lonS = np.nan * np.ones([nlats,nlons],dtype=float)
latS = np.nan * np.ones([nlats,nlons],dtype=float)
bathyS = np.nan * np.ones([nlats,nlons],dtype=float)
c = 0
# Now to reshape the bathy, longitude and latitude into contourable matrices
print('Reshaping data:',time.asctime())
for la in range(0,nlats):
    for lo in range(0,nlons):
        lonS[la,lo] = lon[c]
        latS[la,lo] = lat[c]
        bathyS[la,lo] = bathy[c]
        c+=1

bathyS[bathyS>0]=np.nan         # The positive values (on land) are converted to NaNs
bathyS=-bathyS                  # Flips the bathy values around so that height becomes depth
INPUT.close()

## Reading the Coastline
infile = 'coastline.dat'
INPUT = open(infile,'r')
codes = []
vertices = []
for line in INPUT:
    if line[0] is not '*':
        line.strip()
        lines = line.split(',')
        vertices.append((float(lines[0]),float(lines[1])))
        if int(lines[2])==1:
            codes.append(Path.MOVETO)
        elif int(lines[2])==2:
            codes.append(Path.LINETO)
        elif int(lines[2])==79:
            codes.append(Path.CLOSEPOLY)
INPUT.close()

## Plotting

# plot the Bathy as a shaded background
print('Making Plot:',time.asctime())
plt.set_cmap('Blues')                       # The name of the built-in colour map I want to use. Use Google to find other names (eg: jet, summer, winter, ocean)
FIG = plt.figure()                          # Creates a new figure as well as a handle, called 'FIG' to that figure
AX1 = FIG.add_axes([0.1,0.1,0.9,0.8])       # Creates a new axes insie the figure, FIG, at the position [left, bottom, width, height]

bathymap = plt.pcolor(lonS,latS,bathyS)     # Creates a pcolor plot on the active axes using xdata, ydata and zdata 
AX1.set_ylim([latmin,latmax])               # Sets the Y limits of the axes
AX1.set_xlim([lonmin,lonmax])               # Sets the X limits of the axes
cbar = plt.colorbar(bathymap)               # Creates a colour scale bar to interpret the zdata. This one refers to the pcolor plot called 'bathymap'
cbar.set_label('Depth (m)', labelpad=5)     # Sets a title for the colour bar, and gives the font a padding value so it doesnt overlap any other text
cbar.ax.tick_params(labelsize=8)            # Sets the font size for the labels in the colour bar
bathymap.set_clim(vmin=0,vmax=200)          # Sets the limits of the colour bar. These are currently in metres and refer to the depths.
AX1.set_ylabel('Latitude (Degrees.N)')      # Sets a Y-label for the axes
AX1.set_xlabel('Longitude (Degrees.E)')     # Sets a x-laybel for the axes
AX1.set_title('False Bay')                 # Sets a title for the axes
AX1.set_aspect('equal')                

# Overlay some contour lines on the image
contourplot = plt.contour(\
    lonS,latS,bathyS,                       # The Longitude, Latitude, and Bathy (vertical) data
    levels=[20,50,100,200],                 # The contour levels I want to plot
    colors='k',                             # The colour of the contour lines
    linewidths=0.1,                         # The width of the contour lines
    )
# Label the contours so people know what depth they refer to    
contour_labels = plt.clabel(
    contourplot,                            # The handle to the contour plot               
    inline=0,                               # This means that the contour label must not erase a section of the contour line
    fontsize=2,                             # The fontsize
    fmt='%.0f'                              # A format specifier. This is a float with no digits after the decimal point .... so its similar to an integer
    )

# Overlay a coastline as a greenish coloured patch
landcol = (210/255,227/255,118/255)         # An RGB colour that translates to light grey-green. You can pick your own colours on the web and just write down the RGB triplet
polypath = Path(vertices,codes)             # Creates a Path object called 'polypath'

landpatch = patches.PathPatch(              # Creates a Patch object
    polypath,                               # The name of the'Path object
    facecolor=landcol,                      # The colour of the Patch
    lw=0.1                                  # The width of the line that borders the patch
    )
AX1.add_patch(landpatch)                    # Plots the polygon patch on the Axes
AX1.grid()                                  # Makes a longitude, latitude grid appear on the plot

## Plot the text
TXT = open('Falsebay_landmarks.txt','r')
txtlbl = []
for tl in TXT:
    if tl[0] is not '*':
        tl.strip()
        tlS = tl.split(',')
        x = float(tlS[0])
        y = float(tlS[1])
        txt = '-'+tlS[2]
        txtlbl.append(AX1.text(x,y,txt,
                               verticalalignment='center',
                               fontsize=4))
TXT.close()


## Saving the file
plt.savefig('bathy.png',dpi=600)            # Saves the active figure as a png file, with the specified resolution
print('All done:',time.asctime())

