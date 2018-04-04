import matplotlib.pyplot as plt

from objects import nullImagingOpp
from move_time import movetime
from algoWithDownlink import FCFS
from algoWithDownlink import tabu
from algoWithDownlink import greedy
from algoWithDownlink import Oisempty
from algoWithDownlink import InactiveTime
from algoWithDownlink import greedyWDL

import copy
plt.close("all")
#Null IO
null_IO = nullImagingOpp("nil",None,None,None,None,None,None,None,None,None,None,None,None,None)

def get_rep_list(O):
    rep_lst = []
    for IO  in O:
        rep_lst.append(IO.get_repition())
    return rep_lst

def ResultsForFCFSMulOrbits(O,U,D,Scenario_end):
    orbitPeriod = 5760.0
    orbitCnt = 0
    orbitMaxCnt = int(Scenario_end/orbitPeriod)

    temp_O = copy.copy(O)
    #Check for idle time
    inactivetime = []
    #Printing the Search Space
    lat_initial = []
    longi_initial = []
    for IO in temp_O:
    	lat_initial.append(IO.get_pos()[0])
    	longi_initial.append(IO.get_pos()[1])
    #    print("Name: " + repr(IO.get_name()) + ", Lat, Longi: " + repr(IO.get_pos()) + ", ATW: " + repr(IO.get_ATW()))
    # plt.figure(1)
    # plt.plot(longi_initial,lat_initial, "go")

    while orbitCnt <= orbitMaxCnt and Oisempty(temp_O) == False:
        file = open('Remaining targets for FCFS Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        print("=================================================================")
        print("Results for orbit: " + repr(orbitCnt + 1))
        print("=================================================================")
        S, score = FCFS(temp_O,U,D)
        inactivetime.append(InactiveTime(O,S))
        print("Targets taken by FCFS with score and no. of targets taken: " + repr(score) +", "+ repr(len(S)))

        lat_initial = []
        longi_initial = []
        for IO in temp_O:
            if isinstance(IO,nullImagingOpp):
                continue
            lat_initial.append(IO.get_pos()[0])
            longi_initial.append(IO.get_pos()[1])
            file.write(repr(IO.get_pos()[1]) + ',' + repr(IO.get_pos()[0]) + '\n')
        file.close
        file = open('FCFS results Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        lat_FCFS = []
        longi_FCFS = []
        for i in range(len(S)):
            print("=================================================================")
            print("Satellite is currently at longitude: " + repr(S[i].get_pos()[1]))
            lat_FCFS.append(S[i].get_pos()[0])
       	    longi_FCFS.append(S[i].get_pos()[1])
            print("Target no., Lat, Longi: "+repr(S[i].get_name())+ ", " + repr(S[i].get_pos()))
            print("=================================================================")
            file.write(repr(S[i].get_pos()[1]) + "," + repr(S[i].get_pos()[0]) + "\n")

        rep = get_rep_list(temp_O)
        print("replist" + repr(rep))
        print(len(S))
        for IO in S:
            for i in range(len(temp_O)):
                # if IO == temp_O[i]:
                #     temp_O[i] = null_IO
                #
                if IO == temp_O[i]:
                    temp_O[i].repition -= 1
                if temp_O[i].get_repition() == 0:
                    temp_O[i] = null_IO
            # rep = get_rep_list(temp_O)
            # print("replist" + repr(rep))
        print(temp_O)
        print(O)

        orbitCnt += 1
        file.close
    plt.show()

    print("Done!")

    for IO in temp_O:
        print(isinstance(IO,nullImagingOpp))

    return inactivetime

def ResultsForGreedyMulOrbits(O,U,D,Scenario_end):
    orbitPeriod = 5760.0
    orbitCnt = 0
    orbitMaxCnt = int(Scenario_end/orbitPeriod)

    temp_O = copy.copy(O)
    inactivetime = []
    #Printing the Search Space
    lat_initial = []
    longi_initial = []
    print("Understanding the Search Space")
    for IO in temp_O:
    	lat_initial.append(IO.get_pos()[0])
    	longi_initial.append(IO.get_pos()[1])
    #    print("Name: " + repr(IO.get_name()) + ", Lat, Longi: " + repr(IO.get_pos()) + ", ATW: " + repr(IO.get_ATW()))
    # plt.figure(1)
    # plt.plot(longi_initial,lat_initial, "go")

    while orbitCnt <= orbitMaxCnt and Oisempty(temp_O) == False:
        file = open('Remaining targets for greedy Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        S, score = greedy(temp_O,U,D)
        inactivetime.append(InactiveTime(O,S))
        print("=================================================================")
        print("Results for orbit: " + repr(orbitCnt + 1))
        print("=================================================================")
        print("Targets taken by greedy with score and no. of targets taken: " + repr(score) +", "+ repr(len(S)))

        lat_initial = []
        longi_initial = []
        for IO in temp_O:
            if isinstance(IO,nullImagingOpp):
                continue
            lat_initial.append(IO.get_pos()[0])
            longi_initial.append(IO.get_pos()[1])
            file.write(repr(IO.get_pos()[1]) + ',' + repr(IO.get_pos()[0]) + '\n')
        file.close
        file = open('greedy results Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        lat_greedy = []
        longi_greedy = []
        for i in range(len(S)):
            print(S[i].get_pos()[1])
            lat_greedy.append(S[i].get_pos()[0])
       	    longi_greedy.append(S[i].get_pos()[1])
            print("Target no., Lat, Longi: "+repr(S[i].get_name())+ ", " + repr(S[i].get_pos()))

            file.write(repr(S[i].get_pos()[1]) + "," + repr(S[i].get_pos()[0]) + "\n")

        rep = get_rep_list(temp_O)
        print("replist" + repr(rep))
        print(len(S))
        for IO in S:
            for i in range(len(temp_O)):
                # if IO == temp_O[i]:
                #     temp_O[i] = null_IO
                #
                if IO == temp_O[i]:
                    temp_O[i].repition -= 1
                if temp_O[i].get_repition() == 0:
                    temp_O[i] = null_IO
            # rep = get_rep_list(temp_O)
            # print("replist" + repr(rep))
        print(temp_O)
        print(O)

        orbitCnt += 1
        file.close
    plt.show()

    print("Done!")

    for IO in temp_O:
        print(isinstance(IO,nullImagingOpp))

    return inactivetime


def ResultsForGreedyMulOrbits1(O,U,D,Scenario_end):
    orbitPeriod = 5760.0
    orbitCnt = 0
    orbitMaxCnt = int(Scenario_end/orbitPeriod)

    temp_O = copy.copy(O)
    inactivetime = []
    #Printing the Search Space
    lat_initial = []
    longi_initial = []
    print("Understanding the Search Space")
    for IO in temp_O:
    	lat_initial.append(IO.get_pos()[0])
    	longi_initial.append(IO.get_pos()[1])
    #    print("Name: " + repr(IO.get_name()) + ", Lat, Longi: " + repr(IO.get_pos()) + ", ATW: " + repr(IO.get_ATW()))
    # plt.figure(1)
    # plt.plot(longi_initial,lat_initial, "go")

    while orbitCnt <= orbitMaxCnt and Oisempty(temp_O) == False:
        file = open('Remaining targets for greedy Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        S, score = greedyWDL(temp_O,U,D)
        inactivetime.append(InactiveTime(O,S))
        print("=================================================================")
        print("Results for orbit: " + repr(orbitCnt + 1))
        print("=================================================================")
        print("Targets taken by greedy with score and no. of targets taken: " + repr(score) +", "+ repr(len(S)))

        lat_initial = []
        longi_initial = []
        for IO in temp_O:
            if isinstance(IO,nullImagingOpp):
                continue
            lat_initial.append(IO.get_pos()[0])
            longi_initial.append(IO.get_pos()[1])
            file.write(repr(IO.get_pos()[1]) + ',' + repr(IO.get_pos()[0]) + '\n')
        file.close
        file = open('greedy results Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        lat_greedy = []
        longi_greedy = []
        for i in range(len(S)):
            print(S[i].get_pos()[1])
            lat_greedy.append(S[i].get_pos()[0])
       	    longi_greedy.append(S[i].get_pos()[1])
            print("Target no., Lat, Longi: "+repr(S[i].get_name())+ ", " + repr(S[i].get_pos()))

            file.write(repr(S[i].get_pos()[1]) + "," + repr(S[i].get_pos()[0]) + "\n")

        rep = get_rep_list(temp_O)
        print("replist" + repr(rep))
        print(len(S))
        for IO in S:
            for i in range(len(temp_O)):
                # if IO == temp_O[i]:
                #     temp_O[i] = null_IO
                #
                if IO == temp_O[i]:
                    temp_O[i].repition -= 1
                if temp_O[i].get_repition() == 0:
                    temp_O[i] = null_IO
            # rep = get_rep_list(temp_O)
            # print("replist" + repr(rep))
        print(temp_O)
        print(O)

        orbitCnt += 1
        file.close
    plt.show()

    print("Done!")

    for IO in temp_O:
        print(isinstance(IO,nullImagingOpp))

    return inactivetime

def ResultsForTabuFCFSMulOrbits(O,U,Scenario_end):
    orbitPeriod = 5760.0
    orbitCnt = 0
    orbitMaxCnt = int(Scenario_end/orbitPeriod)

    temp_O = copy.copy(O)
    inactivetime = []
    #Printing the Search Space
    lat_initial = []
    longi_initial = []
    print("Understanding the Search Space")
    for IO in temp_O:
    	lat_initial.append(IO.get_pos()[0])
    	longi_initial.append(IO.get_pos()[1])
    #    print("Name: " + repr(IO.get_name()) + ", Lat, Longi: " + repr(IO.get_pos()) + ", ATW: " + repr(IO.get_ATW()))
    # plt.figure(1)
    # plt.plot(longi_initial,lat_initial, "go")

    while orbitCnt <= orbitMaxCnt and Oisempty(temp_O) == False:
        file = open('Remaining targets for Tabu FCFS Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        t_S2, t_score2 = tabu(temp_O,U,3,2, FCFS)
        Best_score2 = 0
        for i in range(len(t_S2)):
        	if Best_score2 <= t_score2[i]:
        		Best_score2 = t_score2[i]
        		Best_score_index = i

        	Best_S2 = t_S2[Best_score_index]
        inactivetime.append(InactiveTime(O,Best_S2))
        print("=================================================================")
        print("Results for orbit: " + repr(orbitCnt + 1))
        print("=================================================================")
        print("Targets taken by Best Tabu Schedule with FCFS score and targets taken: " + repr(Best_score2) +", " + repr(len(Best_S2)))


        lat_initial = []
        longi_initial = []
        for IO in temp_O:
            if isinstance(IO,nullImagingOpp):
                continue
            lat_initial.append(IO.get_pos()[0])
            longi_initial.append(IO.get_pos()[1])
            file.write(repr(IO.get_pos()[1]) + ',' + repr(IO.get_pos()[0]) + '\n')
        file.close
        file = open('Tabu FCFS results Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        lat_ts2 = []
        longi_ts2 = []
        for i in range(len(Best_S2)):
            lat_ts2.append(Best_S2[i].get_pos()[0])
            longi_ts2.append(Best_S2[i].get_pos()[1])
            print("Target no., Lat, Longi: "+repr(Best_S2[i].get_name())+ ", " + repr(Best_S2[i].get_pos()))
            file.write(repr(Best_S2[i].get_pos()[1]) + "," + repr(Best_S2[i].get_pos()[0]) + "\n")

        rep = get_rep_list(temp_O)
        print("replist" + repr(rep))
        print(len(Best_S2))
        for IO in Best_S2:
            for i in range(len(temp_O)):
                # if IO == temp_O[i]:
                #     temp_O[i] = null_IO
                #
                if IO == temp_O[i]:
                    temp_O[i].repition -= 1
                if temp_O[i].get_repition() == 0:
                    temp_O[i] = null_IO
            # rep = get_rep_list(temp_O)
            # print("replist" + repr(rep))
        print(temp_O)
        print(O)

        orbitCnt += 1
        file.close


def ResultsForTabuGreedyMulOrbits(O,U,Scenario_end):
    orbitPeriod = 5760.0
    orbitCnt = 0
    orbitMaxCnt = int(Scenario_end/orbitPeriod)

    temp_O = copy.copy(O)
    inactivetime = []
    #Printing the Search Space
    lat_initial = []
    longi_initial = []
    print("Understanding the Search Space")
    for IO in temp_O:
    	lat_initial.append(IO.get_pos()[0])
    	longi_initial.append(IO.get_pos()[1])
    #    print("Name: " + repr(IO.get_name()) + ", Lat, Longi: " + repr(IO.get_pos()) + ", ATW: " + repr(IO.get_ATW()))
    # plt.figure(1)
    # plt.plot(longi_initial,lat_initial, "go")

    while orbitCnt <= orbitMaxCnt and Oisempty(temp_O) == False:
        file = open('Remaining targets for Tabu Greedy Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        t_S2, t_score2 = tabu(temp_O,U,3,2, greedy)
        Best_score2 = 0
        for i in range(len(t_S2)):
        	if Best_score2 <= t_score2[i]:
        		Best_score2 = t_score2[i]
        		Best_score_index = i

        	Best_S2 = t_S2[Best_score_index]
        inactivetime.append(InactiveTime(O,Best_S2))
        print("=================================================================")
        print("Results for orbit: " + repr(orbitCnt + 1))
        print("=================================================================")
        print("Targets taken by Best Tabu Schedule with greedy score and targets taken: " + repr(Best_score2) +", " + repr(len(Best_S2)))


        lat_initial = []
        longi_initial = []
        for IO in temp_O:
            if isinstance(IO,nullImagingOpp):
                continue
            lat_initial.append(IO.get_pos()[0])
            longi_initial.append(IO.get_pos()[1])
            file.write(repr(IO.get_pos()[1]) + ',' + repr(IO.get_pos()[0]) + '\n')
        file.close
        file = open('Tabu Greedy results Orbit num ' + repr(orbitCnt+1)+ '.csv','w')
        file.write('x(longi), y(lat)\n')
        lat_ts2 = []
        longi_ts2 = []
        for i in range(len(Best_S2)):
            lat_ts2.append(Best_S2[i].get_pos()[0])
            longi_ts2.append(Best_S2[i].get_pos()[1])
            print("Target no., Lat, Longi: "+repr(Best_S2[i].get_name())+ ", " + repr(Best_S2[i].get_pos()))
            file.write(repr(Best_S2[i].get_pos()[1]) + "," + repr(Best_S2[i].get_pos()[0]) + "\n")

        rep = get_rep_list(temp_O)
        print("replist" + repr(rep))
        print(len(Best_S2))
        for IO in Best_S2:
            for i in range(len(temp_O)):
                # if IO == temp_O[i]:
                #     temp_O[i] = null_IO
                #
                if IO == temp_O[i]:
                    temp_O[i].repition -= 1
                if temp_O[i].get_repition() == 0:
                    temp_O[i] = null_IO
            # rep = get_rep_list(temp_O)
            # print("replist" + repr(rep))
        print(temp_O)
        print(O)

        orbitCnt += 1
        file.close
    plt.show()

    print("Done!")
    return inactivetime
