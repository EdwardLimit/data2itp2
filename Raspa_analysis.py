"""
Script description:

Used for RASPA analysis

Author:Edward Limit
"""

import math
import numpy as np

def averge(step_loading_real, step_energy):
	sum_loading = 0
	sum_energy = 0
	for i in range(len(step_loading_real)):
		sum_loading += step_loading_real[i]
		sum_energy += step_energy[i]

	return [float(sum_loading)/len(step_loading_real), float(sum_energy)/len(step_energy)]


with open('OUTPUT.data') as file_object:  # pls change the output file name to OUTPUT
	lines = file_object.readlines()


step_num = 0  # the total number of step
step_seq = []  # sequence of the step
step_loading = []  # the loading number of every step
step_energy = []  # the final energy
step_loading_real = list()  # the real loading for single compond adsorption


# get total step
for line in lines:
	line = line.split()
	if ('Current' in line) and ("[Init]" not in line) and ("cycle:" in line) and ("Average" not in line):
		step_num = int((int(line[2]) /10000)+1)


iline = 0
while iline < len(lines):
	line = lines[iline].split()
	if ('Current' in line) and ("[Init]" not in line) and ("cycle:" in line) and ("Average" not in line):
		loading_line = lines[iline+13].split()
		energy_line = lines[iline+26].split()
		step_loading.append(loading_line[8])
		step_seq.append(int((int(line[2]) /10000)+1))
		step_energy.append(float(energy_line[3]) * 0.008306341)  # unit change from K to kJ/mol
	iline += 1

for i in range(len(step_loading)):
	l = step_loading[i].split("/")
	step_loading_real.append(int(l[0]))

table = list()
for i in range(len(step_loading)):
	table.append([])
	table[i].append(step_seq[i])
	table[i].append(step_loading_real[i])
	table[i].append(step_energy[i])

Averge_loading, Averge_energy = averge(step_loading_real, step_energy)
print(Averge_loading, Averge_energy)


np.savetxt("LoadingAndEnergy.csv", table, delimiter=",")

"""
Script description:

Used for RASPA analysis

Author:Edward Limit
"""

import math
import numpy as np
import os

with open('Adsorb.pdb') as file_object:  # pls change the output file name to OUTPUT
	lines = file_object.readlines()

with open("AD.pdb", "w") as goal_file:
    for i in lines:
        k = i.split()
        if "CRYST1" in k:
            goal_file.write(str(i))
            break

    for i in lines:
        j = i.split()
        if ("ATOM" and "1" ) in j:
            goal_file.write(i)
"""
Script description:

Used for RASPA analysis

Author:Edward Limit
"""

import math
import numpy as np


def Scale(Energy):
    min = 10000
    max = 0
    for i in range(len(Energy)):
        if abs(Energy[i]) >= max:
            max = abs(Energy[i])
        if abs(Energy[i]) <= min:
            min = abs(Energy[i])
    return min, max


def Scale_divide(min, max, step):
    number = {}
    length = (max - min) / step
    for i in range(step):
        if (str(min + i * length) + "," + str(min + (i+1) * length))  not in number.keys():
            number[str(min + i * length) + "," + str(min + (i+1) * length)] = 0
    return number


def Statistics(number, Energy, step):
    dic = list(number.keys())
    for i in range(10000):
        for j in range(step):
            subdic = dic[j].split(",")
            if float(subdic[0]) <= -1 * Energy[i] < float(subdic[1]):
                number[dic[j]] += 1
    return number


def Final_Statistics(Statistics_result, min, max, step):
    l = list()
    dic = list(Statistics_result.keys())
    length = (max - min) / step
    sum = 0
    for j in range(step):
        sum += Statistics_result[dic[j]]
    for i in range(step):
        l.append([])
        l[i].append(float(min + (i + 0.5) * length))
        l[i].append(Statistics_result[dic[i]])
    return l


energy = np.genfromtxt("LoadingAndEnergy.csv", delimiter=",")
step = 20  # Sampling number
T = 300  # temperature, unit: K

Energy = list()
for i in range(len(energy)):
    Energy.append(energy[i, 2])

Energy = np.array(Energy)

min, max = Scale(Energy)
number = Scale_divide(min, max, step)
Statistics_result = Statistics(number, Energy, step)
Statistics_final = Final_Statistics(Statistics_result, min, max, step)
print(min, max)


np.savetxt("AdsorbSite" + str(step) + ".csv", Statistics_final, delimiter=",")
