from Vehicle import *
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import csv


n_cores = [1,3,5,7,8]
t_simulasi = []
name ='_elapsed.csv'
elapsed = [[] for _ in range(len(n_cores))]

for i in range(len(n_cores)):
    # Read CSV
    with open('parallel' + str(n_cores[i]) + name,mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(i==0):
                t_simulasi.append(float(row[0]))
            elapsed[i].append(float(row[1]))

plt.title('Elapsed Time ')
for i in range(len(n_cores)):
    plt.plot(t_simulasi,elapsed[i],label= str(n_cores[i]) +' Cores')

plt.xlabel('t simulation')
plt.ylabel('elapsed time (s) ')
plt.legend()

last_elapsed = [ el[len(el)-1] for el in elapsed ]
plt.figure()
plt.bar(n_cores, last_elapsed)
for i in range(len(n_cores)):
    plt.text(n_cores[i] - 0.25,last_elapsed[i] + 10,str(round(last_elapsed[i],2)))
plt.yticks(last_elapsed)
plt.xticks(n_cores)

plt.title('Execution Time at t=' + str(int(t_simulasi[len(t_simulasi)-1])))
plt.xlabel('Number of cores')
plt.ylabel('Execution time (s) ')

plt.show()