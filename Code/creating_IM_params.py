from random import random

num = 20
file = open('IM_params.csv','w')

file.write('resource_reqd, tabu_tenure, name, type, lat, longi, payload_reqd, imaging_time, memory_reqd, look_angle_reqd, priority, repition \n')
for i in range(num):
    file.write('[satellite],1,' + repr(i+1) + ',point,' + repr(-5+int(11*random())) + ',' + repr(30+int(100*random())) + ',EO,15,1,45,1,2 \n')
file.close
