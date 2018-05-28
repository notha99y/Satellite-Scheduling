from reading_params import read_IM_file
from reading_params import read_sat_file
from reading_params import generating_IO

import numpy as np
import matplotlib.pyplot as plt

from objects import ImagingOpp
from objects import ImagingMissions
from objects import Satellite

from move_time import movetime
from algo import FCFS
from algo import greedy
from algo import tabu


#from algorithm import tabu#Scenario########
# Scenario_start = 0
# Scenario_end = 10000

#######Scenario########

#######Reading files###########
R = read_IM_file('IM_params_test.csv')
U = read_sat_file('sat_params.csv')
#######Reading files###########

#######Generating O###########
Otemp = generating_IO(R,U)
# for IO in Otemp:
#     print(IO.get_ATW())
O = sorted(Otemp, key=lambda ImagingOpp: ImagingOpp.ATW)
#######Generating O###########

#######Algorithm############ #Remember to tune to objective function
lat_initial = []
longi_initial = []
sat = U[0]
IO = O[0]
test,tes1,test2,test3 = movetime(sat,IO.get_pos())

print(IO.get_pos())
print(sat)
print(IO)
# S,score = greedy(O,U)
# print(len(S))
