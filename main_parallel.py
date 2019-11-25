from Vehicle import *
import math
import numpy as np
import time
import csv
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parameters ==========================================================================
v_params = {
"v_kecil_min" : 80,# km/jam
"v_kecil_max": 100, # km/jam
"v_sedang_min" : 60, # km/jam
"v_sedang_max" : 80, # km/jam
"v_besar_min" : 60, # km/jam
"v_besar_max" : 80 # km/jam
}

v_params_right = {
"v_kecil_min" : 100,# km/jam
"v_kecil_max": 120, # km/jam
"v_sedang_min" : 80, # km/jam
"v_sedang_max" : 100, # km/jam
"v_besar_min" : 80, # km/jam
"v_besar_max" : 100 # km/jam
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
    np.random.seed()
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
    "affected": 80,
    "safety":100,
    "feasible_passing":20,
    "critical":20,
    "extreme": 10
}

def check_speed_limit(mobil):
    pengali = 1000/3600
    if(mobil.posisi.lane==2):
        v_param = v_params
    else:
        v_param = v_params_right
    if(mobil.type==1):
        if(mobil.v > v_param['v_besar_max']):
            mobil.v = pengali * v_param['v_besar_max']

        if(mobil.v < v_param['v_besar_min']):
            mobil.v = pengali * v_param['v_besar_min']

    elif(mobil.type==2):
        if (mobil.v > v_param['v_sedang_max']):
            mobil.v = pengali * v_param['v_sedang_max']

        if (mobil.v < v_param['v_sedang_min']):
            mobil.v = pengali * v_param['v_sedang_min']
    elif(mobil.type==3):
        if (mobil.v > v_param['v_kecil_max']):
            mobil.v = pengali * v_param['v_kecil_max']

        if (mobil.v < v_param['v_kecil_min']):
            mobil.v = pengali * v_param['v_kecil_min']

def speed_rule_travelling_freely(mobil):
    v = np.random.uniform(0,20)
    mobil.update_speed(v)
    check_speed_limit(mobil)

def speed_rule_car_following_with_reference(mobil,status):
    if(status==1 and mobil.vparams.v3!=None):
        deltav = mobil.vparams.v3 - mobil.v
    elif(status==0 and mobil.vparams.v2!=None):
        deltav = mobil.vparams.v2 - mobil.v
    else:
        deltav = 0
    # print('deltav',deltav)
    v = np.random.uniform(0,abs(deltav))
    # print('v_tambahan',v)
    mobil.update_speed_ms(v)
    check_speed_limit(mobil)


def speed_rule_close_car_following(mobil,status):
    if (status == 1 and mobil.vparams.v3!=None):
        deltav = mobil.vparams.v3 - mobil.v
    elif (status == 0 and mobil.vparams.v2 != None):
        deltav = mobil.vparams.v2 - mobil.v
    else:
        deltav = 0
    v = np.random.uniform( -abs(deltav),0 )
    mobil.update_speed_ms(v)
    check_speed_limit(mobil)

def speed_rule_normal_car_following(mobil,status):
    if (status == 1 and mobil.vparams.v3!=None):
        deltav = mobil.vparams.v3 - mobil.v
    elif (status == 0 and mobil.vparams.v2 != None):
        deltav = mobil.vparams.v2 - mobil.v
    else:
        deltav = 0
    v = np.random.uniform(-abs(deltav), abs(deltav))
    mobil.update_speed_ms(v)
    check_speed_limit(mobil)

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
        opp_lane = left_lane

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
    v0 = None  #prev adj
    v1 = None  #prev opp
    v2 = None  #next adj
    v3 = None  #next opp

    for i,m in enumerate(opp_lane):
        if( m.posisi.x > mobil.posisi.x ):
            if(i-1 >= 0 ):
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

    if(idx_mobil-1 >= 0):
        idx_adj_prev = idx_mobil -1
        v0 = lane[idx_adj_prev].v

    # check if in boundary ops lane
    if(idx_next!=-1):
        idx_opp_next = idx_next
        v3 = opp_lane[idx_opp_next].v
        mobil.set_opp_dist(abs(opp_lane[idx_opp_next].posisi.x - mobil.posisi.x))

    if(idx_prev!=-1):
        idx_opp_prev = idx_prev
        v1 = opp_lane[idx_opp_prev].v

    mobil.setVparams( Vparams(v0,v1,v2,v3) )
    mobil.set_adj_dist( abs(lane[idx_adj_next].posisi.x - mobil.posisi.x) )
    if(idx_opp_next != -1 and idx_opp_prev != -1):
        mobil.set_opp_forward_backward( abs(opp_lane[idx_opp_next].posisi.x - opp_lane[idx_opp_prev].posisi.x ) )
    mobil.set_idx_sekitar(idx_adj_next,idx_adj_prev,idx_opp_next,idx_opp_prev)

def check_keluar_road(arr_mobil):
    for m in arr_mobil:
        if(m.isInRoad==False):
            arr_mobil.remove(m)


# Main Simulation
step = int(t_akhir/delta_t)
flows = []
delays = []
arr_mobil = []
speed_1 = []
speed_2 = []
speed_3 = []
delay_1 = []
delay_2 = []
delay_3 = []
elapsed = []
t_simulasi = []
start_time = time.time()

for i in range(step):
    if(rank==0):
        tm = (i+1 * delta_t)
        check_keluar_road(arr_mobil)
        t_simulasi.append(tm)
        if(tm%60==0):
            flows.append( (tm, len(arr_mobil)) )
        # 1. Cek Arrival Mobil Baru dari pintu masuk Tol
        mobil = create_vehicle(prob_arrival, arrival_ratio, v_params)
        if(mobil):
            id_generator = id_generator + 1
            mobil.set_id(id_generator)
            arr_mobil.insert(0,mobil)
            if(mobil.type==1):
                delay_1.append(tm)
            elif(mobil.type==2):
                delay_2.append(tm)
            elif(mobil.type==3):
                delay_3.append(tm)
        # 2. Update Vparams dan Distance Ahead
        (left_lane,right_lane) = split_mobil_per_lane(arr_mobil)
        # print('================================================')
    else:
        left_lane = None
        right_lane = None
        arr_mobil = None
    lanes_comb = comm.bcast([left_lane,right_lane],root=0)
    left_lane = lanes_comb[0]
    right_lane = lanes_comb[1]
    
    if(rank==0):
        chunks = [ [] for _ in range(size) ]
        for j,chunk in enumerate(arr_mobil):
            chunks[j%size].append(chunk)
    else:
        arr_mobil = None
        chunks = None
        
    arr_mobil = comm.scatter(chunks,root=0)
    
    for m in arr_mobil:
        generate_vparams_mobil(m,left_lane,right_lane)
        # print('-------------------')
        if(m.type==1):
            speed_1.append(m.v)
        elif(m.type==2):
            speed_2.append(m.v)
        else:
            speed_3.append(m.v)
        # m.printVehicle()
        # m.vparams.printVparams()
    # 3. Rule based Algorithm
    
    for m in arr_mobil:
        # Cek Lane Mobil
        if(m.posisi.lane==1):
            # Apply Rule Left Lane
            if(m.adj_dist == 0):
                speed_rule_travelling_freely(m)
            else:
                if(m.adj_dist > characteristic_distance['affected'] ):
                    speed_rule_travelling_freely(m)
                else:
                    if(m.vparams.v2 > m.v ):
                        speed_rule_car_following_with_reference(m,0)
                    else:
                        # subjectively overtake?
                        r = np.random.uniform(0,1)
                        # syarat overtake
                        if(r>0.2 and m.adj_dist < characteristic_distance['critical'] and m.opp_dist < characteristic_distance['critical'] and m.opp_dist_forward_backward < characteristic_distance['feasible_passing'] ):
                            # not overtake
                            if (m.adj_dist > characteristic_distance['critical']):
                                speed_rule_normal_car_following(m,0)
                            else:
                                speed_rule_close_car_following(m,0)
                        else:
                            # overtake
                            m.set_id_track(left_lane[m.idx_adj_next].id)
                            m.posisi.lane = 2
                            if(m.opp_dist!=-1 and m.opp_dist < characteristic_distance['affected']):
                                speed_rule_normal_car_following(m,1)
                            else:
                                speed_rule_travelling_freely(m)

        else:
            # Apply Rule Right Lane
            if(m.id_track == left_lane[m.idx_opp_next].id):
                #not yet passed the opp front car
                if(m.adj_dist > characteristic_distance['affected']):
                    speed_rule_travelling_freely(m)
                else:
                    if(m.vparams.v2 != None and m.vparams.v2 > m.v):
                        speed_rule_car_following_with_reference(m,0)
                    else:
                        if(m.adj_dist > characteristic_distance['critical']):
                            speed_rule_normal_car_following(m,1)
                        else:
                            speed_rule_close_car_following(m,1)

            else:
                #has passed the opp front car
                m.set_id_track(None)
                if(m.opp_dist > characteristic_distance['affected']):
                    m.posisi.lane=1
                    speed_rule_travelling_freely(m)
                else:
                    if(m.vparams.v3!=None and m.vparams.v3 > m.v):
                        speed_rule_car_following_with_reference(m,1)
                    else:
                        if(m.opp_dist > characteristic_distance['critical']):
                            speed_rule_normal_car_following(m,1)
                        else:
                            speed_rule_close_car_following(m,1)


        m.posisi.x = m.posisi.x + (m.v * delta_t)
        if(m.posisi.x > panjang_tol ):
            m.set_keluar_road()
    
    arr_mobil = comm.gather(arr_mobil,root=0)
    if(rank==0):
        temp = []
        for m in arr_mobil:
            for mobil in m:
                temp.append(mobil)
        arr_mobil = temp.copy()
        elapsed.append(time.time())
        
    else:
        arr_mobil = None
    
if(rank==0):
    t = [ f[0] for f in flows]
    flow = [ f[1] for f in flows]

    avg1 = sum(speed_1) /  len(speed_1) * 3600/1000
    avg2 = sum(speed_2) /  len(speed_2) * 3600/1000
    avg3 = sum(speed_3) /  len(speed_3) * 3600/1000


    np_delay = np.diff(np.array(delay_1))
    np_delay2 = np.diff(np.array(delay_2))
    np_delay3 = np.diff(np.array(delay_3))

    seq_cars_1 = np.arange(1,np_delay.size+1,1)
    seq_cars_2 = np.arange(1,np_delay2.size+1,1)
    seq_cars_3 = np.arange(1,np_delay3.size+1,1)


    for i in range(len(elapsed)):
        elapsed[i]-= start_time

    with open('parallel'+ str(size) +'_avg_v.csv',mode='w') as csv_time:
        csv_time_writer = csv.writer(csv_time,delimiter=',',quotechar='"')
        csv_time_writer.writerow([ avg1,avg2,avg3 ])

    with open('parallel'+ str(size) +'_elapsed.csv',mode='w') as csv_time:
        csv_time_writer = csv.writer(csv_time,delimiter=',',quotechar='"')
        for i in range(len(elapsed)):
            csv_time_writer.writerow([ t_simulasi[i], elapsed[i]])

    with open('parallel'+ str(size) +'_delay1.csv',mode='w') as csv_time:
        csv_time_writer = csv.writer(csv_time,delimiter=',',quotechar='"')
        for i in range(len(np_delay)):
            csv_time_writer.writerow( [ seq_cars_1[i], np_delay[i] ] )

    with open('parallel'+ str(size) +'_delay2.csv',mode='w') as csv_time:
        csv_time_writer = csv.writer(csv_time,delimiter=',',quotechar='"')
        for i in range(len(np_delay2)):
            csv_time_writer.writerow( [ seq_cars_2[i], np_delay2[i] ] )

    with open('parallel'+ str(size) +'_delay3.csv',mode='w') as csv_time:
        csv_time_writer = csv.writer(csv_time,delimiter=',',quotechar='"')
        for i in range(len(np_delay3)):
            csv_time_writer.writerow( [ seq_cars_3[i], np_delay3[i] ] )

    with open('parallel'+ str(size) +'_flows.csv',mode='w',newline='') as csv_time:
        csv_time_writer = csv.writer(csv_time,delimiter=',',quotechar='"')
        for i in range(len(flow)):
            csv_time_writer.writerow([ t[i],flow[i] ])
