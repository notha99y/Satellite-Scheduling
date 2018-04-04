import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from move_time import movetime as mt
from objects import Satellite

sat = Satellite('T1',1,0.0628,'EO',10,0,10,0,0,550.0)
#Creating a grid
grid_spacing = 0.5
x_range_max = 40.0
x_range_min = 0.0
y_range_max = 5.0
y_range_min = -5.0

no_of_rows = int(abs(y_range_max - y_range_min)/grid_spacing)
no_of_cols = int(abs(x_range_max - x_range_min)/ grid_spacing)

#generating the x values (0.0-40.0)
x_array = []
x_arraytemp = []
x = x_range_min
row = 0.0
while x < x_range_max:
    x_arraytemp.append(x)
    x+=grid_spacing
while row < no_of_rows:
    x_array+=x_arraytemp
    row+=1.0
#generating the y values (-5.0 - 5.0)
y_array = []
y_arraytemp = []
y = y_range_min
col = 0.0

while y < y_range_max:
    y_arraytemp.append(y)
    y_arraytemp1 = y_arraytemp*no_of_cols
    y_array += y_arraytemp1
    y+= grid_spacing
    y_arraytemp = []
#    print(len(y_array))
plt.figure(1)
plt.plot(x_array,y_array, 'go')

#Generating 3d Heat map of the movetime function
z_array_mt=[]
for i in range(len(x_array)):
    t_move, t_move2, pitch, roll = mt(sat,[y_array[i],x_array[i]])
    if t_move2 == False:
        z_array_mt.append(0.0)
    else:
        z_array_mt.append(t_move2)

file = open('3dsurfplots10.csv','w')

for i in range(len(x_array)):
    file.write(repr(x_array[i]) +","+ repr(y_array[i]) +","+ repr(z_array_mt[i]) +'\n')
file.close
print(len(z_array_mt))
plt.show()
