from random import random
import math

num = 1
file = open('sat_params.csv','w')

file.write('name,attitude,ave_angular_speed,payload,memory,max_memory,lat,longi,roll,pitch,yaw,altitude\n')
for i in range(num):
    file.write('T1,1,0.0628,EO,0,8.0,0.0,0.0,0.0,0.0,0.0,550.0\n')
file.close

num2 = 1
file = open('gs_params.csv','w')
file.write('name,lat,longi\n')
for i in range(num2):
    file.write('CRISP,1.3,103.8\n')
    file.write('GREEN,1.3,283.8\n')
    # file.write('ORANGE,-3,90.0\n')
file.close
