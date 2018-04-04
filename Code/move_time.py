#ASSUMPTIONS
#1. No inclinations (and hence no need to update longitude of ascending nodes and no need to rotate to orbital frame)
#2. Only EO sensors considered
#3. All targets only have a default look angle of 45 degrees
#4. Satellite agility only consider simple model
#5. No GS
#6. Satellite has circular orbit (e = 0)
#7. ignoring earth's rotation

#Importing
import math
import numpy as np
# from reading_params import read_IM_file
# from reading_params import read_sat_file
# from reading_params import generating_IO
#
# from objects import ImagingMissions
# from objects import Satellite
# from objects import ImagingOpp
from objects import Downlink

#global variables
a = 6378.137 #Semi major axis of Earth in km
b = 6356.752 #Semi major axis of Earth in km

#function calls
def convert_to_XYZ(lat,longi,height):
    '''
    Transformation from lat,long,height to X,Y,Z
    '''
    alpha = math.radians(lat)
    omega = math.radians(longi)
    h = height #km

    X = (a/(math.sqrt((math.cos(alpha))**2 + (b**2/a**2)*(math.sin(alpha))**2)) + h)*math.cos(alpha)*math.cos(omega)
    Y = (a/(math.sqrt((math.cos(alpha))**2 + (b**2/a**2)*(math.sin(alpha))**2)) + h)*math.cos(alpha)*math.sin(omega)
    Z = (b/(math.sqrt((a**2/b**2)*(math.cos(alpha))**2 + (math.sin(alpha))**2)) + h)*math.sin(alpha)

    return X,Y,Z

def angle2time_new(acc_max,vel_max,theta):
    '''
    ***NEW***
    More accurate modelling of satellite agility
    ***NEW***

    Function that takes in satellite's top acceleration and velocity and angle required to slew abd returns the time
    required to do the slewing.

    Uses slewing rate along the eigen axis
    '''
    time_critical = vel_max/acc_max
    theta_critical = vel_max**2/acc_max

    if theta <= theta_critical:
        time = math.sqrt(4*theta/acc_max)
    elif theta > theta_critical:
        time = 2*time_critical + (theta - theta_critical)/vel_max

    return time

def solving_for_pitch_angle_subtended_by_earth(satellite_angle, pitch_angle,semi_minor,semi_major,sat_vec_norm):
    '''
    Transformation to find the pitch angle subtended by earth for a given satellite state (angle, vector norm, pitch angle)
    and WGS84 model of the earth
    '''
    if pitch_angle < 0:
        pitch_angle = abs(pitch_angle)
    x_sat_gt = semi_major*math.cos(satellite_angle)
    y_sat_gt = semi_minor*math.sin(satellite_angle)

    x_sat = x_sat_gt * sat_vec_norm/math.sqrt(x_sat_gt**2 + y_sat_gt**2)
    y_sat = y_sat_gt * sat_vec_norm/math.sqrt(x_sat_gt**2 + y_sat_gt**2)

    alpha = -x_sat*math.cos(pitch_angle) - y_sat*math.sin(pitch_angle)
    beta = x_sat*math.sin(pitch_angle) - y_sat*math.cos(pitch_angle)

    a1 = semi_minor**2*alpha**2+semi_major**2*beta**2
    b1 = 2*(x_sat*alpha*semi_minor**2 + y_sat*beta*semi_major**2)
    c1 = semi_major**2*y_sat**2+semi_minor**2*x_sat**2 - semi_major**2*semi_minor**2

    cp = (-b1 + math.sqrt(b1**2 - 4*a1*c1))/(2*a1)
    cm = (-b1 - math.sqrt(b1**2 - 4*a1*c1))/(2*a1)
    if cm<= cp:
        c = cm
    else:
        c = cp
    x = x_sat + c*alpha
    y = y_sat + c* beta
    vec = [x,y]
    vec_sat = [x_sat,y_sat]
    temp = np.dot(vec,vec_sat)/np.linalg.norm(vec)/np.linalg.norm(vec_sat)
    if temp > 1:
        temp =1
    theta = math.acos(temp)
    return theta

#main move time function
def movetime(sat,target):
    '''
    =======================
    Main move time function
    =======================
    Takes in a satellite object and an imaging opporunity object and return
    move_time, move_time2, pitch_angle, roll_angle

    move_time: time required to slew
    move_time2: time required to image the targets
    pitch_angle: ending pitch angle of the satellite (used for updating of satellte states)
    row_angle: ending roll angle for the satellite (used for updating of satellite states)
    '''
    #initialising
    tar_lat = math.radians(target.get_pos()[0])
    tar_longi = math.radians(target.get_pos()[1])
    sat_pos = sat.get_orbit_params()
    sat_lat = math.radians(sat_pos[0])
    sat_longi = math.radians(sat_pos[1])

    sat_attitude = sat.get_sat_attitude()
    current_roll = math.radians(sat_attitude[0])
    current_pitch_actual = math.radians(sat_attitude[1])

    height_sat = sat.get_sat_altitude()
    t_stab = 20.0
    # LookAngle = 65.0
    if isinstance(target,Downlink):
        LookAngle = math.radians(65.0)
    else:
        LookAngle = math.radians(45.0)
    Tprime = 1000.0

    sat_ang_spd = (sat.get_ave_angular_speed())*math.pi/180.0
    earth_ang_spd = 7.292115*10**(-5)
    #sat_ang_spd_eff = abs(sat_ang_spd - earth_ang_spd)
    sat_ang_spd_eff = sat_ang_spd

    orbit_radius = a + height_sat

    x,y,z = convert_to_XYZ(tar_lat,tar_longi,0)
    vec = [x,y,z]
    sat_x = orbit_radius * math.cos(sat_longi)
    sat_y = orbit_radius * math.sin(sat_longi)
    sat_vec = [sat_x,sat_y,0]
    vec_norm = np.linalg.norm(vec)
    sat_vec_norm = np.linalg.norm(sat_vec)

    max_look_angle = math.asin(a/(a+height_sat))
    max_look_angle_sub = 2*solving_for_pitch_angle_subtended_by_earth(sat_longi, LookAngle, a, a, sat_vec_norm)
    max_look_time_sat = max_look_angle_sub/sat_ang_spd_eff
    max_look_time = max_look_time_sat + t_stab
    #max_look_time_mano = angle2time_new(0.138, 1.8, math.degrees(max_look_angle))
    #max_look_time = max_look_time_mano + t_stab

    diffinLONG = tar_longi - sat_longi
    if diffinLONG < 0.0:
        Tprime = diffinLONG/sat_ang_spd_eff
        diffinLONG += 2*math.pi
    T = diffinLONG/sat_ang_spd_eff

    test_T_checking = solving_for_pitch_angle_subtended_by_earth(sat_longi, -LookAngle, a, a, sat_vec_norm)/sat_ang_spd_eff
    if abs(Tprime) < test_T_checking:
        T = Tprime
        diffinLONG = diffinLONG - 2.0 * math.pi

    roll_angle_sub = math.atan((a**2/b**2)*math.tan((tar_lat)))
    roll_angle = math.atan(vec_norm * math.sin(roll_angle_sub)/(sat_vec_norm - vec_norm * math.cos(roll_angle_sub)))
    if abs(roll_angle) > abs(LookAngle):
        #print("The required roll angle is larger than the look angle EO")
        #print(math.degrees(roll_angle))
        return False, False, False, False
    delta_roll = roll_angle - current_roll
    roll_time = angle2time_new(0.138, 1.8, math.degrees(abs(delta_roll)))

    T_cond = T - roll_time - t_stab
    #print("T_condition = " + repr(T_cond))

    lim_pitch_angle = math.atan(math.sqrt((math.tan(LookAngle))**2 - (math.tan(roll_angle))**2))
    lim_pitch_angle_sub = solving_for_pitch_angle_subtended_by_earth(roll_time*sat_ang_spd_eff + sat_longi, lim_pitch_angle, a, a, sat_vec_norm)

    pitch_angle_sub = T_cond * sat_ang_spd_eff
    if T_cond < 0 and (abs(pitch_angle_sub) > lim_pitch_angle_sub):
        #print('Unable to capture target as the required backwards pitch angle is larger than the limiting backwards pitch angle')
        return False, False, False, False
    if abs(pitch_angle_sub) > lim_pitch_angle_sub:
        if pitch_angle_sub > 0:
            pitch_angle_sub = lim_pitch_angle_sub
        else:
            pitch_angle_sub = - lim_pitch_angle_sub
        #print('Pitch angle is limited')
    pitch_angle = math.atan(a * math.sin(pitch_angle_sub)/(sat_vec_norm - a * math.cos(pitch_angle_sub)))

    gnd_x = (height_sat/(math.cos(current_roll)))*math.tan(current_pitch_actual)
    current_pitch = math.atan(gnd_x/height_sat)

    delta_pitch = pitch_angle - current_pitch

    if T >= max_look_time or delta_pitch == 0.0:
        pitch_angle_calc = delta_pitch
        #print("delta_pitch = " + repr(delta_pitch))
        #print("T = " + repr(T))
    elif T < max_look_time: #begin iteration
        first_flag = 1;     #to enter 1st time
        move_time = 0;
        move_time2 = 0;
        move_time_old = 0;
        counter = 0;
        pitch_angle_calc = 0;
        upper_bound = 0.95;
        lower_bound = 0.75;
        move_no_change_flag = 1;

        if delta_pitch > 0:     #pitching forward
            scale = 0.5
        else:                   #pitching backward
            scale = 1.1

        condition = move_no_change_flag == 1 and (first_flag == 1 or ((move_time > (upper_bound*move_time2) or move_time < (lower_bound*move_time2)) and abs(pitch_angle_calc + current_pitch)<LookAngle))
        while condition:
            pitch_angle_calc = scale * delta_pitch
            if abs(pitch_angle_calc + current_pitch) > (0.9 * max_look_angle): #0.9*0.5*max_look_angle
                break
##                if scale > 1:
##                    scale = 1.5
##                    pitch_angle_calc = scale * delta_pitch
##                elif scale <= 1:
##                    pitch_angle_calc = scale * delta_pitch / 1.5
            new_look_angle = math.atan(math.sqrt((math.tan(delta_roll))**2 + math.tan(pitch_angle_calc)**2))
            new_look_time = angle2time_new(0.138, 1.8, math.degrees(abs(new_look_angle)))

            move_time = new_look_time + t_stab
            actual_pitch_from_nadir = pitch_angle_calc + current_pitch
            extra_longi_from_pitch = solving_for_pitch_angle_subtended_by_earth(new_look_time*sat_ang_spd_eff + sat_longi, abs(actual_pitch_from_nadir), a, a, sat_vec_norm)
            if actual_pitch_from_nadir < 0:
                extra_longi_from_pitch = - abs(extra_longi_from_pitch)

            move_time2 = T - extra_longi_from_pitch/sat_ang_spd_eff
            move_time_ratio = move_time/move_time2

            if ((move_time_ratio<(0.5*lower_bound)) and delta_pitch>0) or ((move_time_ratio>(2*upper_bound)) and delta_pitch<0):
                scale = 1.5*scale
            elif ((move_time_ratio<(0.75*lower_bound)) and delta_pitch>0) or ((move_time_ratio>(1.5*upper_bound)) and delta_pitch<0):
                scale = 1.25*scale
            elif ((move_time_ratio<(lower_bound)) and delta_pitch>0) or ((move_time_ratio>(upper_bound)) and delta_pitch<0):
                scale = 1.1*scale

            if ((move_time_ratio<(0.5*lower_bound)) and delta_pitch<0) or ((move_time_ratio>(2*upper_bound)) and delta_pitch>0):
                scale = 0.75*scale
            elif ((move_time_ratio<(0.75*lower_bound)) and delta_pitch<0) or ((move_time_ratio>(1.5*upper_bound)) and delta_pitch>0):
                scale = 0.875*scale
            elif ((move_time_ratio<(lower_bound)) and delta_pitch<0) or ((move_time_ratio>(upper_bound)) and delta_pitch>0):
                scale = 0.95*scale

            first_flag = 0
            counter = counter + 1

            move_time_change = abs(move_time - move_time_old)/move_time
            if move_time_change < 0.0001:
                move_no_change_flag = 0
                #print("move no change flag set ----------------------------------")
                #print("scale = " + repr(scale))
                #print("move_time_ratio = " + repr(move_time_ratio))
                #print("pitch_angle_calc = " + repr(pitch_angle_calc))
                #print("delta_pitch = " + repr(delta_pitch))
            move_time_old = move_time

            condition = move_no_change_flag == 1 and (first_flag == 1 or ((move_time > (upper_bound*move_time2) or move_time < (lower_bound*move_time2)) and abs(pitch_angle_calc + current_pitch)<LookAngle))
        #print("iteration counter = " + repr(counter))
        if (pitch_angle_calc + current_pitch) < -lim_pitch_angle:
            #print('Unable to capture target as the required backwards pitch angle is larger than the limiting backwards pitch angle (iteration)')
            return False, False, False, False
        if (pitch_angle_calc + current_pitch) > lim_pitch_angle:    #only if pitching forward
            pitch_angle_calc = lim_pitch_angle - current_pitch
            #print("pitch angle limited (iteration)")
    #recalculating

    #new_look_angle = math.acos(math.cos(roll_angle) * math.cos(pitch_angle_calc))
    new_look_angle = math.atan(math.sqrt((math.tan(delta_roll))**2 + math.tan(pitch_angle_calc)**2))
    new_look_time = angle2time_new(0.138, 1.8, math.degrees(abs(new_look_angle)))

    new_amt_sat_moved = sat_ang_spd_eff * new_look_time
    amt_sat_moved_during_stab = sat_ang_spd_eff * t_stab

    #assigning values to output
    move_time = new_look_time + t_stab
    actual_pitch_from_nadir = pitch_angle_calc + current_pitch
    extra_longi_from_pitch = solving_for_pitch_angle_subtended_by_earth(new_look_time*sat_ang_spd_eff + sat_longi, actual_pitch_from_nadir, a,a, sat_vec_norm)
    if actual_pitch_from_nadir < 0:
        extra_longi_from_pitch = - extra_longi_from_pitch
    longi_moved_in_MT1 = new_amt_sat_moved + amt_sat_moved_during_stab + extra_longi_from_pitch #longi from sat initial nadir pos to boresight at end of MT1 (time to move to look angle)
    excess_longi_after_MT1 = diffinLONG - longi_moved_in_MT1

    #test
    if excess_longi_after_MT1 < 0:
        print('boresight passed target - please check again')
    #end test

    #move_time2 = move_time + excess_longi_after_MT1/effective_angularspeed
    move_time2 = T - extra_longi_from_pitch/sat_ang_spd_eff
    pitch_angle = actual_pitch_from_nadir

    gnd_x = height_sat*math.tan(pitch_angle)
    gnd_y = height_sat*math.tan(roll_angle)
    gnd_roll_hyp = math.sqrt(height_sat**2 + gnd_y**2)
    gnd_pitch_hyp = math.sqrt(height_sat**2 + gnd_x**2)
    pitch_angle_YPR = math.atan(gnd_x/gnd_roll_hyp)
    roll_angle_RPY = math.atan(gnd_y/gnd_pitch_hyp)

    roll_angle = math.degrees(roll_angle)
    pitch_angle = math.degrees(pitch_angle_YPR)

    # if abs(pitch_angle) > 45.0000001:
    #     print("here")
    # #print("target lat = " + repr(pos[0]))
    #print("target longi = " + repr(pos[1]))
    #print("sat longi = " + repr(sat_pos[1]))
    #print("roll = " + repr(roll_angle))
    #print("pitch = " + repr(pitch_angle))
    #print("move_time = " + repr(move_time))
    #print("move_time2 = " + repr(move_time2))

    return move_time, move_time2, pitch_angle, roll_angle
