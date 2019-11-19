from Vehicle import *
import math
import numpy as np

# Parameters ==========================================================================
v_params = {
"v_kecil_min" : 80,# km/jam
"v_kecil_max":100, # km/jam
"v_sedang_min" : 60, # km/jam
"v_sedang_max" : 80, # km/jam
"v_besar_min" : 60, # km/jam
"v_besar_max" : 80 # km/jam
}
rata_rata_volume = 1050 # vehicle per hour
mean_arrival = rata_rata_volume / 3600 # vehicle per second
delta_t = 1
arrival_ratio = {
    "large" : 1,
    "medium" : 2,
    "small" : 6
}
t_akhir = 600
panjang_tol = 144 * 10**3 # meter
id_generator = 0
# ======================================================================================

def prob_poission(lamda,k):
    return ( lamda**k ) * ( math.exp(-k) ) / (math.factorial(k))

prob_arrival = prob_poission(mean_arrival,delta_t) # probability arrival per 1 second

def prob_arrival_car_type(s,m,l):
    total = s + m + l
    return ( l/total, (l+m)/total )

def type_car_generate(ratio):
    r = np.random.uniform(0,1)
    (prob1,prob2) = prob_arrival_car_type(ratio["small"],ratio["medium"],ratio["large"])
    if(r>0 and r <prob1):
        return 1 # large car
    elif(r>= prob1 and r < prob2):
        return 2 # medium car
    elif(r>=prob2 and r < 1):
        return  3 # small car
    else:
        return -1 # invalid input

def car_arrival(prob_arrival,ratio):
    r = np.random.uniform(0,1)
    if(r>prob_arrival):
        return type_car_generate(ratio) # arrive then determine which type of car
    else:
        return -1 # Not Arrive

def create_vehicle(prob_arrival,ratio,v_params):
    type = car_arrival(prob_arrival,ratio)
    if (type==-1):
        return None
    else:
        v = None
        if(type==1):
            v = np.random.uniform(v_params["v_besar_min"],v_params["v_besar_max"])
        elif(type==2):
            v = np.random.uniform(v_params["v_sedang_min"], v_params["v_sedang_max"])
        elif(type==3):
            v = np.random.uniform(v_params["v_kecil_min"], v_params["v_kecil_max"])
        else:
            return None

        return Vehicle( type,v, Posisi(0,1) )

characteristic_distance = {
    "affected": None,
    "safety":None,
    "feasible_passing":None,
    "critical":None,
    "extreme":None
}


def speed_rule_travelling_freely(mobil):
    v = np.random.uniform(-3,3)
    return  mobil.update_speed(v)

def split_mobil_per_lane(arr_mobil):
    left_lane = []
    right_lane = []
    for mobil in arr_mobil:
        if(mobil.posisi.lane == 1):
            left_lane.append(mobil)
        else:
            right_lane.append(mobil)
    return ( left_lane, right_lane)

def generate_vparams_mobil(mobil,left_lane,right_lane):
    lane_mobil = mobil.posisi.lane
    if(lane_mobil==1):
        lane = left_lane
        opp_lane = right_lane
    else:
        lane = right_lane
        opp_lane = right_lane

    idx_mobil = -1
    for i,m in enumerate(lane):
        if(mobil.id == m.id):
            idx_mobil = i

    if(idx_mobil == -1):
        return None

    idx_next = -1
    idx_prev = -1
    idx_adj_prev= -1
    idx_adj_next = -1
    idx_opp_prev= -1
    idx_opp_next = -1
    v0 = None
    v1 = None
    v2 = None
    v3 = None

    for i,m in enumerate(opp_lane):
        if( m.posisi.x > mobil.posisi.x ):
            if(i-1 > 0 ):
                idx_prev = i-1
            else:
                idx_prev =  -1

            if i< len(right_lane):
                idx_next = i
            else:
                idx_next = -1

    # check if in boundary adj lane
    if(idx_mobil+1 < len(lane) ):
        idx_adj_next = idx_mobil+1
        v2 = lane[idx_adj_next].v

    if(idx_mobil-1 > 0):
        idx_adj_prev = idx_mobil -1
        v0 = lane[idx_adj_prev].v

    # check if in boundary ops lane
    if(idx_next!=-1):
        idx_opp_next = idx_next
        v3 = opp_lane[idx_opp_next].v

    if(idx_prev!=-1):
        idx_opp_prev = idx_prev
        v1 = opp_lane[idx_opp_prev].v

    mobil.setVparams( Vparams(v0,v1,v2,v3) )




# Main Simulation
step = int(t_akhir/delta_t)
arr_mobil = []
for i in range(step):
    tm = (i+1 * delta_t)
    # 1. Cek Arrival Mobil Baru dari pintu masuk Tol
    mobil = create_vehicle(prob_arrival, arrival_ratio, v_params)
    if(mobil):
        id_generator = id_generator + 1
        mobil.set_id(id_generator)
        arr_mobil.append(mobil)
    # 2. Update Posisi Mobil Sesuai Rule
    (left_lane,right_lane) = split_mobil_per_lane(arr_mobil)
    for m in arr_mobil:
        generate_vparams_mobil(m,left_lane,right_lane)
        m.printVehicle()
        m.vparams.printVparams()

