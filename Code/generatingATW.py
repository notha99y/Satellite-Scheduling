import csv
from objects import ImagingMissions
from objects import Satellite
from objects import ImagingOpp
from objects import Downlink
from objects import GroundStation
import numpy as np
import matplotlib.pyplot as plt

print("Generating Access... Please Wait")

def plot_FOR(O,D):
    longi = []
    lat = []
    ATW = []

    longi_gs = []
    lat_gs = []
    ATW_gs = []

    f, ax = plt.subplots()

    for DL in D:
        sat = DL.get_satellite()
        aveAngularSpeed = sat.get_ave_angular_speed()
        longi_gs.append(DL.get_pos()[1])
        lat_gs.append(DL.get_pos()[0])
        ATW_radius = (DL.get_ATW()[1] - DL.get_ATW()[0])/2*aveAngularSpeed
        ATW_gs.append(ATW_radius)
    for IO in O:
        sat = IO.get_satellite()
        aveAngularSpeed = sat.get_ave_angular_speed()
        longi.append(IO.get_pos()[1])
        lat.append(IO.get_pos()[0])
        ATW_radius = (IO.get_ATW()[1] - IO.get_ATW()[0])/2*aveAngularSpeed
        ATW.append(ATW_radius)
    #Orbit path
    x= np.linspace(80,120,100)
    y= np.linspace(0,0,100)

    #Field of regard
    for i in range(len(longi_gs)):
        ax.add_artist(plt.Circle((longi_gs[i],0),ATW_gs[i], fill = False, color = 'r'))
    for i in range(len(longi)):
        ax.add_artist(plt.Circle((longi[i],0),ATW[i], fill = False))

    #Plotting
    ax.plot(longi_gs,lat_gs,'y^')
    ax.plot(longi,lat,'go')
    ax.plot(x,y, 'b')
    plt.show()
    f.savefig('FOR.png')

def generating_IO(list_of_IM,list_of_sat):
    O = []
    sat= list_of_sat[0]
    list_of_ATW = []
    list_of_ATW_width = []
    for im in list_of_IM:
        ATW_mid =np.divide(np.dot(im.get_pos(), np.array([0,1])),np.float64(sat.get_ave_angular_speed()))
        list_of_ATW.append(ATW_mid)
        if im.get_pos()[0] == 0:
            ATW_width = np.float64(165)
        else:
            ATW_width = np.multiply(1.0 -np.divide(np.absolute(np.dot(im.get_pos(), np.array([1,0]))),5.2167),165.0)
        list_of_ATW_width.append(ATW_width)
    for i in range(len(list_of_IM)):
        temp_1 = list_of_IM[i].get_resource_reqd()
        temp_2 = int(list_of_IM[i].get_tabu_tenure())
        temp_3 = int(list_of_IM[i].get_name())
        temp_4 = list_of_IM[i].get_size()
        temp_5 = float(list_of_IM[i].lat)
        temp_6 = float(list_of_IM[i].longi)
        temp_7 = list_of_IM[i].get_payload_reqd()
        temp_8 = float(list_of_IM[i].get_imaging_time())
        temp_9 = float(list_of_IM[i].get_memory_reqd())
        temp_10 = float(list_of_IM[i].get_look_angle_reqd())
        temp_11 = i + 1
        temp_12 = list_of_sat[0]
        temp_13 = [list_of_ATW[i] -list_of_ATW_width[i]/2.0 , list_of_ATW[i] + list_of_ATW_width[i]/2.0]
        temp_14 = int(list_of_IM[i].get_priority())
        temp_15 = 0
        temp_16 = int(list_of_IM[i].get_repition())

        temp_IO = ImagingOpp(temp_1,temp_2,temp_3,temp_4,temp_5,temp_6,temp_7,temp_8,temp_9,temp_10,temp_11,temp_12,temp_13,temp_14, temp_15,temp_16)
        O.append(temp_IO)

    print("Access for Imaging Opp done!")
    return O

def generating_DL(list_of_GS, list_of_sat):
    list_of_ATW = []
    list_of_ATW_width = []
    D = []
    dl_rate = 60.0
    for sat in list_of_sat:
        for i in range(len(list_of_GS)):
            gs = list_of_GS[i]
            ATW_mid =np.divide(np.dot(gs.get_pos(), np.array([0,1])),np.float64(sat.get_ave_angular_speed()))
            list_of_ATW.append(ATW_mid)
            if gs.get_pos()[0] == 0:
                ATW_width = np.float64(600)
            else:
                ATW_width = np.multiply(1.0 -np.divide(np.absolute(np.dot(gs.get_pos(), np.array([1,0]))),5.2167),600)
            list_of_ATW_width.append(ATW_width)
        for i in range(len(list_of_GS)):
            gs = list_of_GS[i]
            temp1 = gs.get_name()                       #GS name
            temp2 = "Downlink"                          #downlink name
            temp3 = [sat.get_name(),gs.get_name()]      #resource_reqd
            temp4 = 0                                   #tabu_tenure
            temp5 = gs                                  #GroundStation
            temp6 = gs.get_pos()[0]                     #lat
            temp7 = gs.get_pos()[1]                     #longi
            temp8 = 0.0                                 #downlink_time
            temp9 = sat                                 #satellite
            temp10 = [list_of_ATW[i] -list_of_ATW_width[i]/2.0 , list_of_ATW[i] + list_of_ATW_width[i]/2.0] #ATW
            temp11 = 0.0                                 #score
            temp_Downlink = Downlink(temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9,temp10,temp11)
            D.append(temp_Downlink)
    print("Access for Downlink Opp done!")
    return D
