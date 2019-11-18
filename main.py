from Vehicle import *
import matplotlib.pyplot as plt
import numpy as np

def generate_vehicle(type,v,posisi):
    return Vehicle(type,v,posisi)

def update_posisi_se_lane(posisi,v,delta_t):
    posisi_baru_x = posisi.x + (v * delta_t)
    return Posisi(posisi_baru_x, posisi.lane)

def plot_jalan():
    plt.plot(jalan, np.zeros((jalan.size, 1)) + 1)
    plt.plot(jalan, np.zeros((jalan.size, 1)) + 5)
    plt.plot(jalan, np.zeros((jalan.size, 1)) + 9)



L_jalan = 144 * 10**3  # meter
lebar_lane = 4 # meter
v_kecil = 100 # km/jam
v_sedang = 80 # km/jam
v_besar = 60 # km/jam

t_measured = 2 * 3600 # jam
N = 25 # jumlah mobil
flow = 3600 * N / t_measured # flow: jumlah vehicle / waktu
step = int(3600//flow) +1 # second

arr_mobil = []
t = []
N_mobil = 0

jalan = np.arange(0,L_jalan,1)
print(jalan.size)

# generate kondisi awal
for i in range(0,t_measured,step):
    mobil = generate_vehicle(1,v_kecil,Posisi(0,1))
    N_mobil = N_mobil + 1
    arr_mobil.append(mobil)
    for j in range(N_mobil-1):
        arr_mobil[j].posisi = update_posisi_se_lane(arr_mobil[j].posisi, arr_mobil[j].v, step)
    t.append(i*step)

xs = np.array([mobil.posisi.x for mobil in arr_mobil ])
xlane = np.array([3 for mobil in arr_mobil ])

plt.scatter(xs,xlane,marker='o')
plot_jalan()

# plt.plot(xs,xlane-2)
# plt.plot(xs,xlane + 2)
# plt.plot(xs,xlane + 2 + 4)
# plt.plot(xs,xlane - 2 + 4)
plt.show()




