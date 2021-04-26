"""
Script description
The script converts the data file to an itp file
input command: python data2itp.py XXX.data charge.txt type.txt
and then you could get a XXX.itp file.
We must point out the XXX is the residues name of your system.
The XXX.data must generate by the executable program msi2lmp.exe 
the charge.txt format was show in below:
0.13123

0.12341
0.12313
....
please ensure the charge order is same like the atom order of the XXX.data file
the type.txt format was show in below:
1  opls_1  Si
2  opls_2  O
3  opls_3  H
4  opls_4  C
5  opls_5  C
.....
The first column number have a same order with the XXX.data file the second 
column is the name of forcefield in Gromacs the third column is the name of 
every atoms.
If you have any question you could ask me by Email. 
Best wish for you!!!
"""

import sys

def alist(data):
    with open(data) as data:
        mydata = data.readlines()

    atoms = list()
    bonds = list()
    angles = list()
    dihedrals = list()
    impropers = list()


    for i in mydata:
        myline = i.split()
        if len(myline) >= 1:
            if myline[0] == "Atoms":
                atoms_num = mydata.index(i)
            elif myline[0] == "Bonds":
                bonds_num = mydata.index(i)
            elif myline[0] == "Angles":
                angles_num = mydata.index(i)
            elif myline[0] == "Dihedrals":
                dihedrals_num = mydata.index(i)
            elif myline[0] == "Impropers":
                impropers_num = mydata.index(i)

    for j in range(atoms_num+1, bonds_num):
        atoms_list = mydata[j].split()
        if len(atoms_list) >= 1:
            atoms.append(atoms_list[2])

    bonds_count = 0
    for j in range(bonds_num + 1, angles_num):
        bonds_list = mydata[j].split()
        if len(bonds_list) >= 1:
            bonds.append([])
            bonds[bonds_count].append(bonds_list[2])
            bonds[bonds_count].append(bonds_list[3])
            bonds_count += 1

    angles_count = 0
    for j in range(angles_num + 1, dihedrals_num):
        angles_list = mydata[j].split()
        if len(angles_list) >= 1:
            angles.append([])
            angles[angles_count].append(angles_list[2])
            angles[angles_count].append(angles_list[3])
            angles[angles_count].append(angles_list[4])
            angles_count += 1

    dihedrals_count = 0
    for j in range(dihedrals_num + 1, impropers_num):
        dihedrals_list = mydata[j].split()
        if len(dihedrals_list) >= 1:
            dihedrals.append([])
            dihedrals[dihedrals_count].append(dihedrals_list[2])
            dihedrals[dihedrals_count].append(dihedrals_list[3])
            dihedrals[dihedrals_count].append(dihedrals_list[4])
            dihedrals[dihedrals_count].append(dihedrals_list[5])
            dihedrals_count += 1

    impropers_count = 0
    for j in range(impropers_num + 1, len(mydata)):
        impropers_list = mydata[j].split()
        if len(impropers_list) >= 1:
            impropers.append([])
            impropers[impropers_count].append(impropers_list[2])
            impropers[impropers_count].append(impropers_list[3])
            impropers[impropers_count].append(impropers_list[4])
            impropers[impropers_count].append(impropers_list[5])
            impropers_count += 1

    return atoms, bonds, angles, dihedrals, impropers

def Atom_types(atom_type):
    type_dic = dict()
    name_dic = dict()
    with open(atom_type) as atom_type:
        atom_type_list = atom_type.readlines()
        for i in atom_type_list:
            type_list = i.split()
            type_dic[type_list[0]] = type_list[1]
            name_dic[type_list[0]] = type_list[2]
        return type_dic, name_dic

def main():
    data = sys.argv[1]
    charge = sys.argv[2]

    while True:
        print("Type 1: Periodic type")
        print("Type 3: Ryckaert-Bellemans type")
        print("Type 5: Fourier type")
        print("Type 9: Periodic type")
        dihedrals_type = input("please select the type of your dihedrals type:\n")
        if dihedrals_type in ["1", "3", "5", "9"]:
            break
        print("please input right number. e.g. 1")

    while True:
        print("Type 2: Harnonic type")
        print("Type 4: Periodic type")
        impropers_type = input("please select the type of your impropers dihedrals type:\n")
        if impropers_type in ["2", "4"]:
            break
        print("please input right number. e.g. 2")

    with open(charge) as charge:
        charge_list = charge.readlines()

    atom_type = sys.argv[3]
    type_dic, name_dic = Atom_types(atom_type)

    name = str(data)[:3]
    atoms, bonds, angles, dihedrals, impropers = alist(data)
    itp = open(name + ".itp", "a")
    itp.write("[ moleculetype ]\n")
    itp.write("; Name            nrexcl\n")
    itp.write(name + "    " + "3" + "\n\n")
    itp.write("[ atoms ]\n\t")
    for i in range(len(atoms)):
        itp.write("\t" + str(i+1) + " \t"
                  + type_dic[atoms[i]] + "\t"
                  + " \t" + "1\t" + " \t"
                  + name + "\t" + " \t" + name_dic[atoms[i]] + "\t"
                  + " \t" + "1\t" + " \t" + charge_list[i] + "\t" + "\t")
    itp.write("\n")
    itp.write("\n")
    itp.write("[ bonds ]\n\t")
    for i in range(len(bonds)):
        itp.write("\t" + str(bonds[i][0]) + "\t" + " \t"
                  + str(bonds[i][1]) + "\t" + "\n" + "\t")
    itp.write("\n")
    itp.write("[ angles ]\n\t")
    for i in range(len(angles)):
        itp.write("\t" + str(angles[i][0]) + "\t" + " \t"
                  + str(angles[i][1]) + "\t" + " \t"
                  + str(angles[i][2]) + "\t" + "\n" + "\t")
    itp.write("\n")
    itp.write("[ dihedrals ]\n\t")
    for i in range(len(dihedrals)):
        itp.write("\t" + str(dihedrals[i][0]) + "\t" + " \t"
                  + str(dihedrals[i][1]) + "\t" + " \t"
                  + str(dihedrals[i][2]) + "\t" + " \t"
                  + str(dihedrals[i][3]) + "\t" + " \t" + dihedrals_type + "\n" + "\t")
    itp.write("\n")
    if len(impropers) >= 1:
        itp.write("[ dihedrals ]\n\t")
        for i in range(len(impropers)):
            itp.write("\t" + str(impropers[i][0]) + "\t" + " \t"
                      + str(impropers[i][1]) + "\t" + " \t"
                      + str(impropers[i][2]) + "\t" + " \t"
                      + str(impropers[i][3]) + "\t" + " \t" + impropers_type + "\n" + "\t")
    itp.close()

if __name__ == '__main__':
    main()
