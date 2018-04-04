from reading_params import read_IM_file
from reading_params import read_sat_file
from generatingATW import generating_IO
from move_time import movetime
from objects import ImagingMissions
from objects import Satellite
from objects import ImagingOpp
from objects import nullImagingOpp
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

#stabilization time
stab_time = 30.0
def Oisempty(O):        #Function that returns True if O contains strictly null ImagingOpp
    for IO in O:
        if isinstance(IO,nullImagingOpp) == False:
            return False
    return True
# def testStrategy(sat,D,t,S,dl_rate):


def MCTDLStrategy(sat, D, t, S, dl_rate): #Maximum Capacity Then DownLink Strategy
    print("Satellite " + repr(sat.get_name()) + " has reached maximum memory capacity of "+repr(sat.get_memory())+". Proceeding to finding GS to Downlink...")
    D_temp = []
    D_copy = copy.copy(D)
    D_copy.sort(key = lambda x:x.ATW[0], reverse = False)

    for DL in D_copy:
        if sat.get_memory() == 0.0:
            break
        t_move, t_move2, pitch, roll = movetime(sat, DL)
        if t_move == False:
            print("Unable to Downlink to the following GroundStation: " + repr(DL.get_groundstation().get_name()))
            continue
        t_for_DL = (DL.get_ATW()[1] - (t+t_move2))//dl_rate*dl_rate
        print("DL ATW end: " + repr(DL.get_ATW()[1]))
        print("t: " + repr(t))
        print("t_move2: " + repr(t_move2))
        print(t_for_DL)
        if t_for_DL >= 1.0*dl_rate:
            print("Commencing Downlink to the following GroundStation: " + repr(DL.get_groundstation().get_name()))
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
            DL.downlink_time = t_for_DL
            DL.name1 = "Downlink " + repr(DL.dl_count)
            S.append(DL)
        else:
            print("Unable to Downlink to the following GroundStation1: " + repr(DL.get_groundstation().get_name()))
            print("Will attempt to downlink in the following access to a GroundStation")
            continue

def canDLNot(sat,DL,t,dl_rate):
    t_move, t_move2, pitch, roll = movetime(sat, DL)
    if t_move == False:
        print("Unable to Downlink to the following GroundStation: " + repr(DL.get_name()))
        return False
    t_for_DL = (DL.get_ATW()[1] - (t+t_move2))//dl_rate*dl_rate
    print("DL ATW end: " + repr(DL.get_ATW()[1]))
    print("t: " + repr(t))
    print("t_move2: " + repr(t_move2))
    print(t_for_DL)
    if t_for_DL >= 1.0*dl_rate:
        num_of_imag_dl = t_for_DL//dl_rate
        return True
    else:
        print("Unable to Downlink to the following GroundStation Condition 1: " + repr(DL.get_name()))
        print("Will attempt to downlink in the following access to a GroundStation")
        return False

def InactiveTime(O,S):
    temp = []
    for i in range(len(O)):
        temp.append(0)
    for IO in S:
        for i in range(len(O)):
            if IO == O[i]:
                temp[i] = IO.time_taken
    return temp

def scoring_for_S(S):
    total_score = 0
    for IO in S:
        total_score += IO.score
    return total_score

def FCFS(O,U):
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
        t_move, t_move2, pitch, roll = movetime(sat, IO.get_pos())
        if t_move == False:	#prevents pitching backwards
            continue
        t_end_imaging = t + t_move2 + np.float64(IO.get_imaging_time())
        if np.float64(IO.get_ATW()[1]) >= t_end_imaging:
            S.append(IO)
            IO.score = score_for_IO(IO)
            t = t_end_imaging
            IO.time_taken = t
            sat.longi = t * np.float64(sat.get_ave_angular_speed())
            sat.roll = roll
            sat.pitch = pitch
            sat.yaw = 0 #temporary no updates
            sat.memory = IO.get_memory_reqd
        else:
            continue
        # print(t)
    score = scoring_for_S(S)
    return S, score

def greedy(O,U):
    temp_O = copy.copy(O)
    S = []
    t = np.float64(0)
    for sat in U:
        sat.longi = 0.0
        sat.lat = 0.0
    for IO in O:
        IO.score = 0.0

    def generate_best_ngb(temp_O):
        Best_i = 0
        Best_score = -100.0
        score = []
        for i in range(len(temp_O)):
            IO = temp_O[i]
            if isinstance(IO,nullImagingOpp):
#                print("IO is null")
                continue
            sat = IO.get_satellite()
            t_move, t_move2, pitch, roll = movetime(sat, IO.get_pos())
            if t_move == False:   #This means it fails either one of the three conditions specified from movetime function
#                print("Sat is pitching backwards")
                continue
            IO.score = score_for_IO(IO)
            score.append(IO.score)
            if Best_score <= IO.score:
                Best_score = IO.score
                Best_i = i
        Best_ngb = temp_O[Best_i]
        # print("Scores: " + repr(score))
        # print("Best score: " + repr(Best_ngb.get_score())+ "Best_ngb's index: " + repr(Best_i))

        return Best_ngb, Best_i

    for i in range(len(temp_O)):
#        print("Going through elem: " + repr(i) + "==============================")
        IO, Best_i = generate_best_ngb(temp_O)
        if isinstance(IO,nullImagingOpp):
#            print("no more solutions found, breaking from loop")
            break

        t_move, t_move2, pitch, roll = movetime(sat, IO.get_pos())
        t_end_imaging = t + t_move2 + np.float64(IO.get_imaging_time())

        if np.float64(IO.get_ATW()[1]) >= t_end_imaging:
            S.append(IO)
            IO.score = score_for_IO(IO)
            t = t_end_imaging
            IO.time_taken = t
            sat.longi = t * np.float64(sat.get_ave_angular_speed())
            sat.roll = roll
            sat.pitch = pitch
            sat.yaw = 0 #temporary nothing
            sat.memory = IO.get_memory_reqd()
            temp_O[Best_i] = null_IO
            # print("iteration: " + repr(i))
            # print("satellite's attitude, (roll, pitch): " + repr(roll) +", " + repr(pitch))
            # print("target taken, (name, lat, long): " + repr(IO.get_name1()) +", "+ repr(IO.get_pos()))
        else:
            # print("Didnt get target as TW constraint un met")
#            print("TW constraint not met, looking at the next best neightbour")
            temp_O[Best_i] = null_IO
#        print("temp_O: " + repr(temp_O))
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
