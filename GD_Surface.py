"""
Using for swelling process of polymer in solution.
the format of input file is ：

  Column 1          Column 2               Column 3
Cordination      Polymer density        Solution denstiy
XXXX                XXXX                    XXXX

For example:
    0.0944089            0                 1120.84
    0.283227             0                 1002.95
    0.472044             0                  942.686
    0.660862             0                 1155.16
    0.84968              0                 1078.08
    1.0385               0                 1078.31
    1.22732              0                 1004.59
    1.41613              0                 1018.85
    1.60495              0                 1056.4
    1.79377              0                 1034.67
    1.98259              0                 1049.84
    2.1714               0                 1051.42
    2.36022              0                 1099.08
    2.54904              15.0559           1078.23

Input temple: python GD_Surface.py in_file_name a1 a2 b1 b2 avg_1 avg_2

The funcitional of this script:

1. 
"""



import sys
import math

def GDS(density_distribution, a1, a2, b1, b2):
    with open(density_distribution) as fp:
        line = fp.readlines()

    a1_label = 0
    a2_label = 0
    b1_label = 0
    b2_label = 0

    density = list()

    for i in line:
        myline = i.split()
        if abs(float(myline[0]) - a1) < 0.1 :
            a1_label = myline[0]
        elif abs(float(myline[0]) - a2) < 0.1:
            a2_label = myline[0]
        elif abs(float(myline[0]) - b1) < 0.1:
            b1_label = myline[0]
        elif abs(float(myline[0]) - b2) < 0.1:
            b2_label = myline[0]
        density.append(float(myline[1]) + float(myline[2]))

    count = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0

    for i in line:
        count += 1
        num = i.split()
        if num[0] == a1_label:
            count_1 = count
        elif num[0] == b1_label:
            count_2 = count
        elif num[0] == b2_label:
            count_3 = count
        elif num[0] == a2_label:
            count_4 = count

    avg_1 = (sum(density[:count_1]) / count_1 + sum(density[count_4:]) / (len(density) - count_4 +1)) * 0.5
    avg_2 = sum(density[count_2:][:(count_3 - count_2)]) / (count_3 - count_2)
    print(avg_2, avg_1)
    avg_12 = sum(density[count_1:][:(count_2 - count_1)]) / (count_2 - count_1)
    avg_23 = sum(density[count_3:][:(count_4 - count_3)]) / (count_4 - count_3)
    s1 = (avg_12 * (float(b1) - float(a1)) + avg_1 * float(a1) - avg_2 * float(b1)) / (avg_1 - avg_2)
    s2 = (avg_23 * (float(a2) - float(b2)) + avg_2 * float(b2) - avg_1 * float(a2)) / (avg_2 - avg_1)

    return s1, s2, b1_label, b2_label

def averge(ave, b1, b2):
    with open(ave) as fp:
        line = fp.readlines()

        sum = 0
        count = 0
        for i in line:
            myline = i.split()
            if ( float(myline[0]) >= float(b1) ) and ( float(myline[0]) <= float(b2) ):
                sum += float(myline[1])
                count += 1

        ave_density = sum / count

    return ave_density

def fit(file, density, s1, s2, b1, b2):
    s1 = float(s1)
    s2 = float(s2)
    b1 = float(b1)
    b2 = float(b2)

    sigema = ((s2 - s1) - (b2 - b1)) / 6

    with open(file) as fp:
        line = fp.readlines()

    density_fit = list()
    for i in line:
        myline = i.split()
        a = density * ((math.erf((float(myline[0]) - s1) / (sigema * 1.41))) - (math.erf((float(myline[0]) - s2) / (sigema * 1.41)))) * 0.5
        density_fit.append(a)

    file_fit = open("fit_density.xvg", "a")

    for i in density_fit:
        file_fit.write(str(i) + "\n")

    file_fit.close()


def dissolution_degree(dissolution, s1, s2):
    with open(dissolution) as fp:
        line = fp.readlines()

    s1_label = 0
    s2_label = 0

    density1 = list()

    for i in line:
        myline = i.split()
        if abs(float(myline[0]) - s1) < 0.1 :
            s1_label = myline[0]
        elif abs(float(myline[0]) - s2) < 0.1:
            s2_label = myline[0]
        density1.append(float(myline[2]))

    count = 0
    count1 = 0
    count2 = 0

    for i in line:
        count += 1
        num = i.split()
        if num[0] == s1_label:
            count1 = count
        elif num[0] == s2_label:
            count2 = count

    m = sum(density1[count1:][:(count2 - count1)]) / (count2 - count1)

    return m


if __name__ == '__main__':
    density_distribution = sys.argv[1]
    a1 = float(sys.argv[2])
    a2 = float(sys.argv[3])
    b1 = float(sys.argv[4])
    b2 = float(sys.argv[5])
    s1, s2, bulk1, bulk2 = GDS(density_distribution, a1, a2, b1, b2)
    ave_density = averge(density_distribution, bulk1, bulk2)
    fit(density_distribution, ave_density, s1, s2, bulk1, bulk2)
    m = dissolution_degree(density_distribution, s1, s2)

    print("The surface1 is %f" % s1)
    print("The surface2 is %f" % s2)
    print("The surface of bulk1 is %s" % bulk1)
    print("The surface of bulk2 is %s" % bulk2)
    print("The fitting averge density is %s" % ave_density)
    print("The dissolution degree is %s" % m)
