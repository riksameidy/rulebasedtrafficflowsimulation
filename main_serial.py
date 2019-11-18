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
t_akhir = 7200
panjang_tol = 144 * 10**3 # meter
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

# Main Simulation
step = int(t_akhir/delta_t)
arr_mobil = []
for i in range(step):
    tm = (i+1 * delta_t)
    # 1. Cek Arrival Mobil Baru dari pintu masuk Tol
    mobil = create_vehicle(prob_arrival, arrival_ratio, v_params)
    if(mobil):
        arr_mobil.append(mobil)
    # 2. Update Posisi Mobil
