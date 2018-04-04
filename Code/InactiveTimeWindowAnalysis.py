from reading_params import read_IM_file
from reading_params import read_sat_file
from reading_params import generating_IO

from resultschecking import ResultsForFCFSMulOrbits
from resultschecking import ResultsForGreedyMulOrbits
from resultschecking import ResultsForTabuFCFSMulOrbits
from resultschecking import ResultsForTabuGreedyMulOrbits

import numpy as np
import matplotlib.pyplot as plt

from objects import ImagingOpp
from objects import ImagingMissions
from objects import Satellite

from algo import movetime
from algo import FCFS
from algo import tabu
from algo import greedy
from algo import InactiveTime

def DayToSecConvert(days):
	return days*24.0*3600.0
def SecToHrsConvert(secs):
    return secs/3600.0
def SecToOrbitsConvert(secs,Sat_period):
    return secs/Sat_period
days = 2.0
Scenario_start = 0
Scenario_end = DayToSecConvert(days)
sat_period = 5760.0
#######Scenario########

#######Reading files###########
R = read_IM_file('IM_params.csv')
U = read_sat_file('sat_params.csv')
#######Reading files###########

#######Generating O###########
Otemp = generating_IO(R,U)
# for IO in Otemp:
#     print(IO.get_ATW())
O = sorted(Otemp, key=lambda ImagingOpp: ImagingOpp.ATW)

#test = plottingResultsForFCFSMulOrbits(O,U,Scenario_end)
# test = plottingResultsForGreedyMulOrbits(O,U,Scenario_end)
test = plottingResultsForTabuGreedyMulOrbits(O,U,Scenario_end)
#Adjusting to the orbit
for i in range(len(test)):
    for j in range(len(test[i])):
        add = sat_period * (i)
        if test[i][j] != 0:
            test[i][j] += add
#Adjusting to the orbit

#Getting the delta
delta = []
template_endTimes = []
for i in range(len(O)):
    delta.append([])
    template_endTimes.append(0)
print(len(delta))
for i in range(len(test)):
    if i ==0:
        for j in range(len(test[i])):
            if test[i][j] != 0:
                delta[j].append(test[i][j])
        continue
    for j in range(len(test[i])):
        if test[i-1][j] != 0:
            template_endTimes[j] = test[i-1][j]
    for j in range(len(test[i])):
        if test[i][j] != 0:
            delta[j].append(test[i][j] - template_endTimes[j])
print("========================================================================")
for orbs in test:
    print(orbs)
mean = []
for i in range(len(delta)):
    for j in range(len(delta[i])):
        delta[i][j] = SecToOrbitsConvert(delta[i][j], sat_period)
    delta[i].append(sum(delta[i])/len(delta[i]))
    mean.append(sum(delta[i])/len(delta[i]))
print(delta)
plt.figure(1)
plt.plot(delta, 'o')
plt.figure(2)
plt.plot(mean,'co')
plt.show()
