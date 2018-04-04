from objects_superclass import Task
from objects_superclass import Resource

class ImagingMissions(Task):
    im_count = 0
    tabu_freq = 0
    def __init__(self, resource_reqd, tabu_tenure, name,size, lat, longi, payload_reqd, imaging_time, memory_reqd, look_angle_reqd, priority, repition):
        self.resource_reqd = resource_reqd
        self.tabu_tenure = tabu_tenure
        self.name = name
        self.size = size
        self.lat = lat
        self.longi = longi
        self.payload_reqd = payload_reqd
        self.imaging_time = imaging_time
        self.memory_reqd = memory_reqd
        self.look_angle_reqd = look_angle_reqd
        self.priority = priority
        self.repition =repition
        ImagingMissions.im_count += 1

    def __repr__(self):
        return "0"

    def get_name(self):
        return self.name
    def get_size(self):
        return self.size
    def get_pos(self):
        return [float(self.lat),float(self.longi)]
    def get_payload_reqd(self):
        return self.payload_reqd
    def get_imaging_time(self):
        return float(self.imaging_time)
    def get_memory_reqd(self):
        return float(self.memory_reqd)
    def get_look_angle_reqd(self):
        return float(self.look_angle_reqd)
    def get_priority(self):
        return float(self.priority)
    def get_repition(self):
        return float(self.repition)

class Satellite(Resource):
    sat_count = 0
    def __init__(self,name,attitude,ave_angular_speed,payload,memory,max_memory,lat,longi,roll,pitch,yaw,altitude):
        self.name = name
        self.attitude = attitude
        self.ave_angular_speed = ave_angular_speed
        self.payload = payload
        self.memory = memory
        self.max_memory = max_memory
        self.lat = lat
        self.longi = longi
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.altitude = altitude
        Satellite.sat_count += 1

    def get_name(self):
        return self.name
    def get_attitude(self):
        return self.attitude
    def get_ave_angular_speed(self):
        return float(self.ave_angular_speed)
    def get_payload(self):
        return self.payload
    def get_memory(self):
        return float(self.memory)
    def get_max_memory(self):
        return float(self.max_memory)
    def get_orbit_params(self):
        return [float(self.lat),float(self.longi)]
    def get_sat_attitude(self):
        return [float(self.roll),float(self.pitch), float(self.yaw)]
    def get_sat_altitude(self):
        return float(self.altitude)

class GroundStation(Resource):
    gs_count = 0
    def __init__(self, name, lat, longi):
        self.name = name
        self.lat = lat
        self.longi = longi

    def get_name(self):
        return self.name
    def get_pos(self):
        return [float(self.lat),float(self.longi)]

class ImagingOpp(ImagingMissions):
    im_opp_count = 0
    tabu_freq = 0
    time_taken = 0
    def __init__(self, resource_reqd, tabu_tenure, name, size, lat,longi, payload_reqd, imaging_time, memory_reqd, look_angle_reqd,  name1, satellite, ATW,priority, score, repition):
        self.resource_reqd = resource_reqd
        self.tabu_tenure = tabu_tenure
        self.name = name
        self.size = size
        self.lat = lat
        self.longi = longi
        self.payload_reqd = payload_reqd
        self.imaging_time = imaging_time
        self.memory_reqd = memory_reqd
        self.look_angle_reqd = look_angle_reqd
        self.priority = priority
        self.name1 = name1
        self.satellite = satellite
        self.ATW = ATW
        self.score = score
        self.repition =repition
        ImagingOpp.im_opp_count += 1

    def __repr__(self):
        return "1"

    def get_name1(self):
        return self.name1
    def get_satellite(self):
        return self.satellite
    def get_ATW(self):
        return self.ATW
    def get_score(self):
        return self.score


class nullImagingOpp(ImagingMissions):
    im_opp_count = 0
    tabu_freq = 0
    def __init__(self, resource_reqd, tabu_tenure, name, size, lat,longi, payload_reqd, imaging_time, memory_reqd, look_angle_reqd,  name1, satellite, ATW,priority = 1, score = 0, repition = 0):
        self.resource_reqd = resource_reqd #1
        self.tabu_tenure = tabu_tenure #2
        self.name = name #3
        self.size = size #4
        self.lat = lat #5
        self.longi = longi #6
        self.payload_reqd = payload_reqd #7
        self.imaging_time = imaging_time #8
        self.memory_reqd = memory_reqd #9
        self.look_angle_reqd = look_angle_reqd #10
        self.priority = priority #11
        self.name1 = name1 #12
        self.satellite = satellite #13
        self.ATW = ATW #14
        self.score = score #15
        self.repition =repition #16
        ImagingOpp.im_opp_count += 1

    def __repr__(self):
        return "0"

    def get_name1(self):
        return self.name1
    def get_satellite(self):
        return self.satellite
    def get_ATW(self):
        return self.ATW
    def get_score(self):
        return self.score

class Downlink(Task):
    dl_count = 0
    tabu_freq = 0
    def __init__(self, name, name1, resource_reqd, tabu_tenure, groundstation, lat, longi, downlink_time, satellite, ATW, score):
        self.name = name
        self.name1 = name1
        self.resource_reqd = resource_reqd
        self.tabu_tenure = tabu_tenure
        self.groundstation = groundstation
        self.lat = lat
        self.longi = longi
        self.downlink_time = downlink_time
        self.satellite = satellite
        self.ATW = ATW
        self.score = score
        Downlink.dl_count+= 1
    def get_name(self):
        return self.name
    def get_name1(self):
        return self.name1
    def get_groundstation(self):
        return self.groundstation
    def get_resource_reqd(self):
        return self.resource_reqd
    def get_pos(self):
        return [float(self.lat), float(self.longi)]
    def get_downlink_time(self):
        return self.downlink_time
    def get_satellite(self):
        return self.satellite
    def get_ATW(self):
        return self.ATW
    def get_score(self):
        return self.score
#Testing
# test_IM = ImagingMissions(['satellite'],1,'1',[1,2],'EO',5,1,45,1)
# print(test_IM)
# print(test_IM.im_count)
# print("-------------------------------------------------------------------------")
# test_sat = Satellite('T1',[0.1,0.1,0.1],3.75,'EO',8,[1,1])
# print(test_sat)
# print(test_sat.sat_count)
# print(test_sat.get_name())
# print('-------------------------------------------------------------------------')
# test_IMopp = ImagingOpp(['satellite'],1,'1',[1,2],'EO',5,1,45,1,'1',test_sat,[100,120])
# print(test_IMopp)
# print(test_IMopp.im_opp_count)
