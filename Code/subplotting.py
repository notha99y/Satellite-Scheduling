import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import csv
import math
import os
# from mpl_toolkits.basemap import Basemap

style.use('ggplot')
# style.use('fivethirtyeight')
# plt.close('all')

def read_results(filename):
    x = []
    y = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in spamreader:
            if firstline:
                firstline = False
                continue
            x.append(row[0])
            y.append(row[1])

    return x,y

def read_gs_params(filename):
    x = []
    y = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in spamreader:
            if firstline:
                firstline = False
                continue
            x.append(row[2])
            y.append(row[1])

    return x,y
###############Algo File################
# algoName = 'FCFS'
algoName = 'greedy'
# algoName = 'Tabu FCFS'
# algoName = 'Tabu Greedy'
###############Algo File################

###########Number of Orbits############
numberOfOrbits = 8
###########Number of Orbits############
#Reading files
path = os.path.join(os.getcwd()[:-4],'config')

xgs,ygs = read_gs_params(os.path.join(path,'gs_params.csv'))
x_tak = []
y_tak = []
x_tar = []
y_tar = []

for i in range(numberOfOrbits):
    x_tak_temp, y_tak_temp = read_results(algoName + " results Orbit num " + repr(i + 1) + ".csv")
    x_tar_temp, y_tar_temp = read_results("Remaining targets for " + algoName + " Orbit num " + repr(i + 1) + ".csv")

    x_tak.append(x_tak_temp)
    y_tak.append(y_tak_temp)
    x_tar.append(x_tar_temp)
    y_tar.append(y_tar_temp)

# row and column sharing
x= np.linspace(0,360,500)
y= np.linspace(0,0,500)

counter = 0
for i in range(numberOfOrbits//10):
    f, axs = plt.subplots(2, 5, sharex='all', sharey='all')
    axs = axs.ravel()

    for j in range(10):

        axs[j].plot(x,y,'b', label = 'Satellite Path')
        axs[j].plot(x_tar[counter + j], y_tar[counter + j], 'go', label = 'Targets')
        axs[j].plot(x_tak[counter + j], y_tak[counter + j], 'ro', label = 'Targets Taken')
        axs[j].plot(x_tak[counter + j], y_tak[counter + j], 'r')

        axs[j].plot(xgs,ygs,'y^', label = 'Ground Station')
        axs[j].set_xlabel('Longi (deg)')
        axs[j].set_ylabel('Lat (deg)')
        axs[j].set_xlim([0,361])
        axs[j].set_ylim([-10,11])
        axs[j].set_xticks([x1 for x1 in range(0,361,25)])
        axs[j].set_yticks([y1 for y1 in range(-10,11,2)])
        axs[j].set_title('Orbit ' + repr(counter+j+1))

        # m = Basemap(projection='mill', llcrnrlat=-90,urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, ax = axs[j])
        # m.drawcoastlines()
        # m.fillcontinents(color = 'coral', lake_color = 'aqua')
        # m.drawmapboundary(fill_color='aqua')
    counter += 10


if numberOfOrbits%10 != 0:
    f,axs = plt.subplots(2, int(np.ceil((numberOfOrbits%10.0)/2.0)), sharex='all', sharey='all')
    axs = axs.ravel()
    counter = numberOfOrbits//10 * 10
    # print(counter)

    for i in range(numberOfOrbits%10):
        axs[i].plot(x_tar[counter + i], y_tar[counter + i], 'go', label = 'Targets')
        axs[i].plot(x_tak[counter + i], y_tak[counter + i], 'ro', label = 'Targets Taken')
        axs[i].plot(x_tak[counter + i], y_tak[counter + i], 'r')
        axs[i].plot(x,y,'b', label = "Satellite Path")
        axs[i].plot(xgs,ygs,'y^', label = "Ground Station")
        axs[i].set_xlabel('Longi (deg)')
        axs[i].set_ylabel('Lat (deg)')
        axs[i].set_xlim([0,361])
        axs[i].set_ylim([-10,11])
        axs[i].set_xticks([x1 for x1 in range(0,361,30)])
        axs[i].set_yticks([y1 for y1 in range(-10,11,2)])
        axs[i].set_title('Orbit ' + repr(counter+i+1))

        # m = Basemap(projection='mill', llcrnrlat=-90,urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, ax = axs[i])
        # m.drawcoastlines()
        # m.fillcontinents(color = 'coral', lake_color = 'aqua')
        # m.drawmapboundary(fill_color='aqua')

plt.legend()
plt.show()
