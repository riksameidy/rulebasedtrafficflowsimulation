from Vehicle import *
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import csv


core_max = 8
t_simulasi = []
name ='_elapsed.csv'
elapsed = [[] for _ in range(core_max)]

for i in range(core_max):
    # Read CSV
    with open('parallel' + str(i+1) + name,mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(i==0):
                t_simulasi.append(float(row[0]))
            elapsed[i].append(float(row[1]))

print(elapsed)

plt.title('Elapsed Time ')
for i in range(core_max):
    plt.plot(t_simulasi,elapsed[i],label= str(i+1) +' Cores')

plt.xlabel('t simulation')
plt.ylabel('elapsed time (s) ')
plt.legend()


plt.show()