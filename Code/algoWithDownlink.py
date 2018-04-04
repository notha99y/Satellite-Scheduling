from move_time import movetime
from random import random
from objects import ImagingMissions
from objects import Satellite
from objects import ImagingOpp
from objects import nullImagingOpp
from objects import Downlink
from algo import MCTDLStrategy
from algo import canDLNot
import numpy as np
import copy

#Null IO
null_IO = nullImagingOpp("nil",None,None,None,None,None,None,None,None,None,None,None,None,None)
#Tuning
k1 = 1      #movetime
k2 = 0      #lookangle
k3 = 0      #num_of_imag_opp
k4 = 0      #priority
k5 = 0      #score_early
k6 = 1      #eveness
threshold = 7
#stabilization time
stab_time = 30.0
def Oisempty(O):        #Function that returns True if O contains strictly null ImagingOpp
    for IO in O:
        if isinstance(IO,nullImagingOpp) == False:
            return False
    return True
# #Testing
# #######Reading files###########
# R = read_IM_file('IM_params.csv')
# U = read_sat_file('sat_params.csv')
# #######Reading files###########
#
# #######Generating O###########
# emptyO = []
# i = 0
# while i <= 10:
#     emptyO.append(null_IO)
#     i+= 1
# Otemp = generating_IO(R,U)
# O = sorted(Otemp, key=lambda ImagingOpp: ImagingOpp.ATW)
# #######Generating O###########
# print(Oisempty(O))
# print(Oisempty(emptyO))
# print(O)
# print(emptyO)
def InactiveTime(O,S):
    temp = []
    for i in range(len(O)):
        temp.append(0)
    for IO in S:
        for i in range(len(O)):
            if IO == O[i]:
                temp[i] = IO.time_taken
    return temp

def score_for_task(task):
    score = 0
    scoreFromMoveTime = []
    scoreFromEven = []
    def movetime_score(task):
        if isinstance(task, Downlink):
            sat = task.get_satellite()
            t_move, t_move2, pitch, roll = movetime(sat, task)
            # alpha = 1
            alpha = (sat.get_memory() - threshold + 1) * 1
            score = (4.0 - 3.0*(t_move2)/5760.0)*alpha
            return score
        elif isinstance(task, ImagingOpp):
            sat = task.get_satellite()
            t_move, t_move2, pitch, roll = movetime(sat, task)
            score = 4.0 - 3.0*(t_move2)/5760.0
            return score
        else:
            print(type(task))
            score = 0
            return score

    # def time_left_score(task):
    #     if isinstance(task,ImagingOpp):
    #         score = 0
    #     elif isinstance(task,Downlink):
    #         score = 0
    #     else:
    #         print(type(task))
    #         score = 0
    #     return score

    # def movetime_score(task):
    #     score = 4.0 - 3.0*(movetime1(task.get_satellite(), task.get_pos()))/10.0
    #     return score
    def even_score(task):
        if isinstance(task,Downlink):
            score = 0
        else:
            rep = task.get_repition()
            ave_rep = 3
            if ave_rep - rep == 1:
                score = -0.1
            elif ave_rep - rep == 2:
                score = -0.2
            else:
                score = 0
        return score

    def look_angle_score(task):
        score = 1
        return score
    def num_of_imag_opp_score(task):
        score = 1
        return score
    def priority_score(task):
        score = 1
        return score
    def early_score(task):
        score = 1
        return score

    s1 = movetime_score(task)
    s2 = look_angle_score(task)
    s3 = num_of_imag_opp_score(task)
    s4 = priority_score(task)
    s5 = early_score(task)
    s6 = even_score(task)

    scoreFromMoveTime.append(k1*s1)
    scoreFromEven.append(k6*s6)

    score = np.multiply(np.float64(k1), np.float64(s1)) + np.multiply(np.float64(k2), np.float64(s2)) + np.multiply(np.float64(k3), np.float64(s3)) + np.multiply(np.float64(k4), np.float64(s4)) \
    + np.multiply(np.float64(k5), np.float64(s5)) + np.multiply(np.float64(k6), np.float64(s6))
    #print("score from MT: "+ repr(scoreFromMoveTime))
    # print("score from even: "+ repr(scoreFromEven))
    return score

def scoring_for_S(S):
    total_score = 0
    for IO in S:
        total_score += IO.score
    return total_score

def FCFS(O,U,D):
    S = []
    score = []
    t = np.float64(0)
    for sat in U:
        sat.longi = 0
        sat.lat = 0
    for IO in O:
        IO.score = 0.0
    for IO in O:
        if isinstance(IO,nullImagingOpp):
            continue
        # print("HERE!!!" + repr(IO))
        sat = IO.get_satellite()
        #print("Here " + repr(IO.get_pos()))
        # print(sat.longi)
        # print("HERE!!!" + repr(sat))
        #t_move, t_move2 = movetime(sat, IO.get_pos())
        t_move, t_move2, pitch, roll = movetime(sat, IO)
        if t_move == False:
            continue
        t_end_imaging = t + t_move2 + np.float64(IO.get_imaging_time())
        if np.float64(IO.get_ATW()[1]) >= t_end_imaging and sat.get_memory() + IO.get_memory_reqd() <= sat.get_max_memory():
            S.append(IO)
            IO.score = score_for_task(IO)
            t = t_end_imaging
            IO.time_taken = t
            sat.longi = t * np.float64(sat.get_ave_angular_speed())
            sat.roll = roll
            sat.pitch = pitch
            sat.yaw = 0.0 #temporary no updates
            sat.memory += IO.get_memory_reqd()
        #######################DL Strategy####################
        if sat.get_memory() >= sat.get_max_memory():
            test = MCTDLStrategy(sat,D,t,S, 60.0)
            # test = testStrategy(sat,D,t,S,60.0)
            break
        #######################DL Strategy####################
        else:
            continue
        # print(t)
    score = scoring_for_S(S)
    return S, score

def greedy(O,U,D):
    temp_O = copy.copy(O)
    temp_D = copy.copy(D)
    S = []
    t = np.float64(0)
    for sat in U:
        sat.longi = 0.0
        sat.lat = 0.0
    for IO in temp_O:
        IO.score = 0.0
    for DL in temp_D:
        DL.score = 0.0
    def generate_best_ngb(temp_list):
        Best_i = 0
        Best_score = -100.0
        score = []
        for i in range(len(temp_list)):
            task = temp_list[i]
            if isinstance(task,nullImagingOpp):
                continue
            sat = task.get_satellite()
            t_move, t_move2, pitch, roll = movetime(sat, task)
            if t_move == False:   #This means it fails either one of the three conditions specified from movetime function
                continue
            task.score = score_for_task(task)
            score.append(task.score)
            if Best_score <= task.score:
                Best_score = task.score
                Best_i = i
        Best_ngb = temp_list[Best_i]
        return Best_ngb, Best_i

    for i in range(len(temp_O)):
#        print("Going through elem: " + repr(i) + "==============================")
        IO, Best_i = generate_best_ngb(temp_O)

        if isinstance(IO,nullImagingOpp):
#            print("no more solutions found, breaking from loop")
            break
        t_move, t_move2, pitch, roll = movetime(sat, IO)
        t_end_imaging = t + t_move2 + np.float64(IO.get_imaging_time())

        if np.float64(IO.get_ATW()[1]) >= t_end_imaging and sat.get_memory() + IO.get_memory_reqd() <= sat.get_max_memory():
            S.append(IO)
            IO.score = score_for_task(IO)
            t = t_end_imaging
            IO.time_taken = t
            sat.longi = t * np.float64(sat.get_ave_angular_speed())
            sat.roll = roll
            sat.pitch = pitch
            sat.yaw = 0 #temporary nothing
            sat.memory += IO.get_memory_reqd()
            temp_O[Best_i] = null_IO
            print("Satellite memory is: " + repr(sat.get_memory()))
            # print("iteration: " + repr(i))
            # print("satellite's attitude, (roll, pitch): " + repr(roll) +", " + repr(pitch))
            # print("target taken, (name, lat, long): " + repr(IO.get_name1()) +", "+ repr(IO.get_pos()))
        else:
            print("Didnt get target as TW constraint un met")
            temp_O[Best_i] = null_IO
#        print("temp_O: " + repr(temp_O))

        #######################DL Strategy####################
        dl_rate = 60.0
        if sat.get_memory() >= sat.get_max_memory():
            test = MCTDLStrategy(sat,D,t,S, 60.0)
            # test = testStrategy(sat,D,t,S,60.0)
            break
        #######################DL Strategy####################

    score = scoring_for_S(S)
    return S, score

def greedyWDL(O,U,D):
    temp_O = copy.copy(O)
    S = []
    t = np.float64(0)
    for sat in U:
        sat.longi = 0.0
        sat.lat = 0.0
    for IO in O:
        IO.score = 0.0
    for DL in D:
        DL.score = 0.0

    def generate_best_ngb(temp_list):
        Best_i = 0
        Best_score = -100.0
        score = []
        for i in range(len(temp_list)):
            task = temp_list[i]
            if isinstance(task,nullImagingOpp):
                continue
            sat = task.get_satellite()
            t_move, t_move2, pitch, roll = movetime(sat, task)
            if t_move == False:   #This means it fails either one of the three conditions specified from movetime function
                continue
            task.score = score_for_task(task)
            score.append(task.score)
            if Best_score <= task.score:
                Best_score = task.score
                Best_i = i
        Best_ngb = temp_list[Best_i]
        return Best_ngb, Best_i

#iteration starts#############################################################
    for i in range(len(temp_O)):
        temp_D = copy.copy(D)

        IO, Best_i = generate_best_ngb(temp_O)
        if isinstance(IO,nullImagingOpp):
            break
        print("viable IO under investigation: " + repr(IO.get_pos()))
        t_move, t_move2, pitch, roll = movetime(sat, IO)
        t_end_imaging = t + t_move2 + np.float64(IO.get_imaging_time())

        if np.float64(IO.get_ATW()[1]) >= t_end_imaging and sat.get_memory() + IO.get_memory_reqd() <= sat.get_max_memory():
            #######################DL Strategy####################
            print("#######################DL Strategy####################")
            dl_rate = 60.0
            if sat.get_memory() >= threshold:
                print("Satellite memory, " +repr(sat.get_memory()) + " is above or equal to the fixed threshold, " +repr(threshold) + ". Deciding if there is a need to DL")
                ######Calculate score#######
                print("Choosing the best GS to DL to...")
                best_DL, best_i = generate_best_ngb(temp_D)
                print(best_DL.get_name())
                print("Checking if " + repr(best_DL.get_name()) + " has enough access to perform DL")
                if canDLNot(sat,best_DL,t,60.0):
                    print("Able to DL to the following GS: " + repr(best_DL.get_name()) )
                    print("Deciding if we were to DL or continue taking IO.")
                    print(best_DL.get_score())
                    print(IO.get_score())
                    if IO.get_score() > best_DL.get_score():
                        print("Score for IO is larger than DL. Hence algo decides to continue to Image")
                        S.append(IO)
                        t = t_end_imaging
                        IO.time_taken = t
                        sat.longi = t * np.float64(sat.get_ave_angular_speed())
                        sat.roll = roll
                        sat.pitch = pitch
                        sat.yaw = 0 #temporary nothing
                        sat.memory += IO.get_memory_reqd()
                        temp_O[Best_i] = null_IO
                    elif IO.get_score()<= best_DL.get_score():
                        print("Score for DL is larger than IO. Hence algo decides to DL")
                        t_move, t_move2, pitch, roll = movetime(sat, best_DL)
                        t_for_DL = (best_DL.get_ATW()[1] - (t+t_move2))//dl_rate*dl_rate
                        print(t_for_DL)
                        if t_for_DL >= 1.0*dl_rate:
                            print("Commencing Downlink to the following GroundStation: " + repr(best_DL.get_groundstation().get_name()))
                            num_of_imag_dl = t_for_DL//dl_rate
                            if num_of_imag_dl > sat.get_memory():
                                print("Memory of Satellite is at: " + repr(sat.get_memory()) + " and there are ample time to downlink all the images.")
                                num_of_imag_dl = sat.get_memory()
                            print("Number of images downlinked is: " + repr(num_of_imag_dl))
                            sat.memory -= num_of_imag_dl
                            print("Satillte memory is now: " + repr(sat.get_memory()))
                            t = t+t_move2 +t_for_DL
                            sat.longi = t*np.float64(sat.get_ave_angular_speed())
                            t_move, t_move2, pitch, roll = movetime(sat,DL)
                            sat.roll = roll
                            sat.pitch = pitch
                            best_DL.downlink_time = t_for_DL
                            best_DL.name1 = "Downlink " + repr(best_DL.dl_count)
                            S.append(DL)
                    else:
                        print("Shouldnt come in here. got bug. please check. Score of IO == Score of DL")
                else:
                    S.append(IO)
                    t = t_end_imaging
                    IO.time_taken = t
                    sat.longi = t * np.float64(sat.get_ave_angular_speed())
                    sat.roll = roll
                    sat.pitch = pitch
                    sat.yaw = 0 #temporary nothing
                    sat.memory += IO.get_memory_reqd()
                    temp_O[Best_i] = null_IO
            #######################DL Strategy####################
            else:
                S.append(IO)
                t = t_end_imaging
                IO.time_taken = t
                sat.longi = t * np.float64(sat.get_ave_angular_speed())
                sat.roll = roll
                sat.pitch = pitch
                sat.yaw = 0 #temporary nothing
                sat.memory += IO.get_memory_reqd()
                temp_O[Best_i] = null_IO
        else:
            print("Didnt get target as TW constraint un met")
            temp_O[Best_i] = null_IO

    score = scoring_for_S(S)
    return S, score

def tabu(O, U, no_of_iteration, no_of_tabu_elems, nested_heuristic):
    temp_O = copy.copy(O)
    list_of_S = []
    list_of_Total_score = []
    tabu_list = []

    S, score = nested_heuristic(temp_O,U)   #First solution
    # print("here")
    # print(len(S))
    # print(score)
    list_of_S.append(S)
    list_of_Total_score.append(score)

    # print("swee1")
    for i in range(len(O)):         #Initializing Tabu List
        tabu_list.append(null_IO)
        temp_O[i].tabu_tenure = 1
        temp_O[i].tabu_freq = 0
        temp_O[i].time_taken = 0
    for i in range(no_of_iteration):
        list_of_Ngbrs_score = []
        for j in range(len(O)):     #Generating ngbrhood
            temp2_O = copy.copy(temp_O)
            temp2_O[j] = null_IO
            new_S, new_score = nested_heuristic(temp2_O,U)
            list_of_Ngbrs_score.append(new_score)
        # print("swee2")
        count = 0
        while count < no_of_tabu_elems:
            Best_score = -100                      #Choosing Best neightbour
            for j in range(len(O)):
                if list_of_Ngbrs_score[j] > Best_score and temp_O[j] != null_IO:
                    Best_score = list_of_Ngbrs_score[j]
                    Best_j = j
            # print("swee3")
            # print("=========iteration=======")
            # print(Best_j)
            tabu_elem = temp_O[Best_j]
            tabu_elem.tabu_tenure += 2 + tabu_elem.get_tabu_freq()
            tabu_elem.tabu_freq += 1
            tabu_list[Best_j] = tabu_elem
            temp_O[Best_j] = null_IO #tabu-ed
            count += 1
            # print("tabu iteration==============================================")
            # print("count for iteration: "+ repr(count))
            # print("current template schedule: "+repr(temp_O))
            # print("tabu list: "+repr(tabu_list))

        # print("swee4")
        S, score = nested_heuristic(temp_O, U)
        # print(S)
        # print("here2")
        # print(len(S))
        # print(score)
        list_of_S.append(S)
        list_of_Total_score.append(score)

        # print("swee5")
        # print("starting O: " + repr(temp_O))
        # print("starting M: " + repr(tabu_list))
        for j in range(len(tabu_list)):  #Updating Tabu list and performing tenure expiry
            # print("IO no: "+repr(tabu_list[j].get_name())+" tenure: " + repr(tabu_list[j].get_tabu_tenure()))
            if tabu_list[j] != null_IO:
                tabu_list[j].tabu_tenure_expiry()
                # print("Here")
                # print("IO no: "+repr(tabu_list[j].get_name())+" tenure: " + repr(tabu_list[j].get_tabu_tenure()))
            if tabu_list[j].get_tabu_tenure() == 0:
                temp_O[j] = tabu_list[j]
                tabu_list[j] = null_IO
                # print("Here2")
        #
        # print("S: " + repr(S))
        # print("O: " + repr(temp_O))
        # print("M: " + repr(tabu_list))
    return list_of_S, list_of_Total_score
