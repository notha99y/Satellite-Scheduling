import csv
from objects import ImagingMissions
from objects import Satellite
from objects import ImagingOpp
from objects import GroundStation
import numpy as np

def read_IM_file(filename):
    R = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in spamreader:
            if firstline:
                firstline = False
                continue
            temp_1 = row[0]		#resource_reqd
            temp_2 = row[1]		#tabu_tenure
            temp_3 = row[2]		#name
            temp_4 = row[3]		#type
            temp_5 = row[4]		#lat
            temp_6 = row[5]		#longi
            temp_7 = row[6]		#payload_reqd
            temp_8 = row[7]		#imaging_time
            temp_9 = row[8]		#memory_reqd
            temp_10 = row[9]	#look_angle_reqd
            temp_11 = row[10]	#priority
            temp_12 = row[11]   #repition
            temp_IM = ImagingMissions(temp_1,temp_2,temp_3,temp_4,temp_5,temp_6,temp_7,temp_8,temp_9,temp_10,temp_11,temp_12)
            R.append(temp_IM)
    return R

def read_sat_file(filename):
    U = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in spamreader:
            if firstline:
                firstline = False
                continue
            temp_1 = row[0]		#name
            temp_2 = row[1]		#attitude
            temp_3 = row[2]		#ave_angular_speed
            temp_4 = row[3]		#payload
            temp_5 = row[4]		#memory
            temp_6 = row[5]     #max memory
            temp_7 = row[6]		#lat
            temp_8 = row[7]		#longi
            temp_9 = row[8]     #roll
            temp_10 = row[9]     #pitch
            temp_11 = row[10]    #yaw
            temp_12 = row[11]   #altitude

            temp_sat = Satellite(temp_1,temp_2,temp_3,temp_4,float(temp_5),temp_6,temp_7,temp_8,temp_9,temp_10,temp_11, temp_12)
            U.append(temp_sat)
    return U

def read_GS_file(filename):
    G = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',')
        firstline = True
        for row in spamreader:
            if firstline:
                firstline = False
                continue
            temp_1 = row[0]
            temp_2 = row[1]
            temp_3 = row[2]
            temp_GS = GroundStation(temp_1,temp_2,temp_3)
            G.append(temp_GS)
    return G

# file = open('imagingtask_params.csv','r')
# for line in file:
#     print('---------------------------------------------------------------------')
#     print(line)
