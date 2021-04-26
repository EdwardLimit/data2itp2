import sys

def SolutionDegree(my_data, error):
    with open(my_data) as data:
        SD_data = data.readlines()

    distance = list()
    solution = list()
    solute = list()

    for i in SD_data:
        data_line = i.split()
        distance.append(data_line[0])
        solution.append(data_line[1])
        solute.append(data_line[2])

    # print(distance)
    # print(solute)
    # print(solution)

    d = float(distance[1]) - float(distance[0])

    label_left = 0

    while abs(float(solute[label_left]) - float(solution[label_left])) >= int(error):
        label_left += 1
        print(label_left)
    print("the left interface is %s" % distance[label_left])


    label_right = len(SD_data) - 1

    while abs(float(solute[label_right]) - float(solution[label_right])) >= int(error):
        label_right -= 1
    print("the right interface is %s" % distance[label_right])

    SD = 0
    for i in range(label_left, label_right + 1):
        SD += d * float(solute[i])

    return SD / (float(distance[label_right]) - float(distance[label_left]))

def main():
    my_data = sys.argv[1]
    print(my_data)
    error = sys.argv[2]
    print(error)
    SD = SolutionDegree(my_data, error)
    print(SD)

if __name__ == '__main__':
    main()
