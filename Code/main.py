'''
Main Script to running scheduler (last updated 18 Dec 2016)

Written by Tan Ren Jie
'''

import os
import numpy as np
import matplotlib.pyplot as plt

from reading_params import read_IM_file
from reading_params import read_sat_file
from reading_params import read_GS_file

from generatingATW import generating_IO
from generatingATW import generating_DL
from generatingATW import plot_FOR
# from algoWithDownlink import FCFS
from resultschecking import ResultsForFCFSMulOrbits
from resultschecking import ResultsForGreedyMulOrbits
from resultschecking import ResultsForGreedyMulOrbits1
from resultschecking import ResultsForTabuFCFSMulOrbits
from resultschecking import ResultsForTabuGreedyMulOrbits

from algoWithDownlink import greedyWDL
from algoWithDownlink import greedy
from algoWithDownlink import score_for_task

########Scenario########
def DayToSecConvert(days):
	return days*24.0*3600.0
days = 1
Scenario_start = 0
Scenario_end = DayToSecConvert(days)
#######Scenario########

#######Reading files###########
path = os.path.join(os.getcwd()[:-4],'config')
R = read_IM_file(os.path.join(path,'IM_params.csv'))
U = read_sat_file(os.path.join(path,'sat_params.csv'))
G = read_GS_file(os.path.join(path,'gs_params.csv'))
#######Reading files###########
# for gs in G:
# 	print(gs.get_name())
#######Generating O & D###########
Otemp = generating_IO(R,U)
# for IO in Otemp:
#     print(IO.get_ATW())
O = sorted(Otemp, key=lambda ImagingOpp: ImagingOpp.ATW)
D = generating_DL(G,U)

#######Generating O & D###########
# plot_FOR(O,D)
######Showing ATW ###########
# S, score = FCFS(O,U,D)
# print(S)
######Showing ATW ###########
#######Algorithm############
#Remember to tune to objective function

# test = ResultsForFCFSMulOrbits(O,U,D,Scenario_end)
test = ResultsForGreedyMulOrbits(O,U,D,Scenario_end)
# test = ResultsForTabuFCFSMulOrbits(O,U,D,Scenario_end)
# test = ResultsForTabuGreedyMulOrbits(O,U,D,Scenario_end)
#######Algorithm############

#######Results#############

#######Results#############

# print(S)
# print(len(S))
# print(sat.get_orbit_params())
# for IO in O:
#     print(IO.get_ATW())
