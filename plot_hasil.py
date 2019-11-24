from Vehicle import *
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

t_simulasi = []
elapsed = []
avg_v = []
delay1 = []
delay2 = []
delay3 = []
seq_car_1 = []
seq_car_2 = []
seq_car_3 = []

# load hasil simulasi
with open('serial_elapsed.csv',mode='r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        t_simulasi.append(float(row[0]) )
        elapsed.append(float(row[1]) )

with open('serial_avg_v.csv',mode='r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        avg_v.append( float(row[0]) )
        avg_v.append( float(row[1]) )
        avg_v.append( float(row[2]) )

with open('serial_delay1.csv',mode='r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        seq_car_1.append(float(row[0]))
        delay1.append(float(row[1]))

with open('serial_delay2.csv',mode='r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        seq_car_2.append(float(row[0]))
        delay2.append(float(row[1]))

with open('serial_delay3.csv',mode='r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        seq_car_3.append(float(row[0]))
        delay3.append(float(row[1]))

print('v rata-rata: ',avg_v)

# Plot Hasil Simulasi

plt.plot(t_simulasi,elapsed)
plt.title('Elapsed Time ')
plt.xlabel('t simulation')
plt.ylabel('elapsed time (s) ')

plt.figure()
plt.plot( seq_car_1,delay1 , color='r')
plt.title('Delay Mobil Besar')
plt.xlabel('Sequence Number of Car')
plt.ylabel('Delay time (s) ')


plt.figure()
plt.plot( seq_car_2,delay2 , color='g')
plt.title('Delay Mobil Sedang')
plt.xlabel('Sequence Number of Car')
plt.ylabel('Delay time (s) ')

plt.figure()
plt.plot( seq_car_3,delay3 , color='b')
plt.title('Delay Mobil Kecil')
plt.xlabel('Sequence Number of Car')
plt.ylabel('Delay time (s) ')

plt.show()