#! /usr/bin/python
import sys
import random
import time


def val(size, vicinity, flow, distance):
    value = 0
    for i in range(size):
        for j in range(size):
            value += int(flow[i][j]) * int(distance[vicinity[i]][vicinity[j]])

    return value


def generate_vicinity_random(size):
    v = list(set(range(0, size)))
    for i in range(size):
        rand = random.choice(v)
        v.remove(rand)
        v.append(rand)
    return v


def permute_vicinity(vicinity, first, second):
    temp = vicinity[first]
    vicinity[first] = vicinity[second]
    vicinity[second] = temp
    return vicinity


def main(argv):
        # my code here
    if len(argv) > 1:
        f = open(sys.argv[1], 'r')
    else:
        f = sys.stdin
    if len(argv) > 2:
        maxtime = float(sys.argv[2])
    else:
        maxtime = 50

    size = int(f.readline().strip())
    f.readline()

    flow = [[0 for x in range(size)] for x in range(size)]
    distance = [[0 for x in range(size)] for x in range(size)]
    vicinity = [0 for x in range(size)]
    for counter, line in enumerate(f):
        bufer = line.split()
        if bufer == '':
            continue
        if counter < size+1:
            # print "primera Matriz"
            for col, number in enumerate(bufer):
                flow[counter][col] = number
        else:
            # print "Segunda Matriz"
            for col, number in enumerate(bufer):
                distance[counter-(size+1)][col] = number

        # print bufer
    vicinity = generate_vicinity_random(size)
    # vicinity = [7,5,12,2,1,3,9,11,10,6,8,4]
    # for n     in range(len(vicinity)):
        # vicinity[n] = vicinity[n] -1
    # print vicinity
    # print val(size, vicinity, flow, distance)
    vicinityValue = val(size, vicinity, flow, distance)
    while time.clock() < maxtime:
        # print time.clock()
        for i in range(size):
            for counter, j in enumerate(range(size)):
                if counter == 0:
                    j+=1
                newVicinity = permute_vicinity(vicinity, i, j)
                newVicinityValue = val(size, newVicinity, flow, distance)
                print newVicinity, newVicinityValue
                if vicinityValue > newVicinityValue:
                    vicinity = newVicinity
                    vicinityValue = newVicinityValue

    print "Mejor Vecindad Encontrada: " , vicinity
    print "Mejor valor: ", vicinityValue
if __name__ == "__main__":
    main(sys.argv)
