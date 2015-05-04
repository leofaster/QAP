#! /usr/bin/python
import sys
import random
import time
import itertools


def val(size, vicinity, flow, distance):
    value = 0
    for i in range(size):
        for j in range(size):
            # print i, j
            value += int(flow[i][j]) * int(distance[vicinity[i]][vicinity[j]])

    return value


def generate_vicinity_random(size):
    v = list(set(range(0, size)))
    for i in range(size):
        rand = random.choice(v)
        v.remove(rand)
        v.append(rand)

    return v


def permute_min_local_random(vicinity, position):
    swapPosition = random.choice(range(position, len(vicinity)))
    tmp = vicinity[position]
    vicinity[position] = vicinity[swapPosition]
    vicinity[swapPosition] = tmp

    return vicinity


def permute_min_local_next(vicinity, position, swich):
    tmp = vicinity[position]
    vicinity[position] = vicinity[swich]
    vicinity[swich] = tmp

    return vicinity


def permute_vicinity(vicinity, first, second):
    temp = vicinity[first]
    vicinity[first] = vicinity[second]
    vicinity[second] = temp

    return vicinity


def obtain_min_random(vicinity, vicinityValue, size, flow, distance, maxtime):
    position = 0
    laps = 0
    while time.clock() < maxtime:
        laps += 1
        newVicinity = permute_min_local_random(vicinity, position)
        newVicinityValue = val(size, newVicinity, flow, distance)
        if vicinityValue > newVicinityValue:
            vicinity = newVicinity
            vicinityValue = newVicinityValue
            position += 1

    print "Mejor valor: ", vicinityValue
    print "Tiempo de corrida: ", time.clock()
    print "Iteraciones: ", laps


def obtain_min_random_next(
    vicinity,
    vicinityValue,
    size,
    flow,
    distance,
    maxtime
):

    position = 0
    sw = 1
    laps = 0
    while time.clock() < maxtime and position < size:
        laps += 1
        newVicinity = permute_min_local_next(vicinity, position, sw)
        newVicinityValue = val(size, newVicinity, flow, distance)

        if vicinityValue > newVicinityValue:
            vicinity = newVicinity
            vicinityValue = newVicinityValue
            position += 1
            sw += 1
        else:
            if sw + 1 >= size:
                if (position + 1) >= size:
                    position = 0
                    sw = 1
                else:
                    position += 1
                    if position + 1 >= size:
                        sw = 0
                    else:
                        sw = position + 1
            else:
                sw += 1

    print "Mejor valor: ", vicinityValue
    print "Tiempo de corrida: ", time.clock()
    print "Iteraciones: ", laps


def obtain_min_force(
    vicinity, vicinityValue, size, flow, distance, maxtime
):
    # allVicinity = list(itertools.permutations(vicinity))
    i = 0
    j = size-1
    laps = 0
    # counter = 0
    while time.clock() < maxtime and j > 0 and i < size:
        laps += 1
        # newVicinity = allVicinity[counter]  #(vicinity, i, j)
        newVicinity = permute_vicinity(vicinity, i, j)
        newVicinityValue = val(size, newVicinity, flow, distance)
        if vicinityValue > newVicinityValue:
            vicinity = newVicinity
            vicinityValue = newVicinityValue
        if j <= 1:
            i += 1
            j = size - 1
        else:
            j -= 1
        # counter += 1

    print "Mejor valor: ", vicinityValue
    print "Tiempo de corrida: ", time.clock()
    print "Iteraciones: ", laps


def main(argv):
    if len(argv) > 1:
        f = open(sys.argv[1], 'r')
    else:
        f = sys.stdin
    if len(argv) > 2:
        maxtime = float(sys.argv[2])
    else:
        maxtime = 10

    size = int(f.readline().strip())

    f.readline()  # We read and leave this line

    # Initializate the variables
    vicinity = [0 for x in range(size)]
    i = 0
    matrix = []
    for line in f:
        y = line.strip()
        if y == '':
            continue
        for z in y.split():
            if i % size == 0:
                matrix.append([])
            matrix[-1].append(int(z))
            i += 1
    assert i == 2 * size * size
    flow = matrix[:size]
    distance = matrix[size:]

    vicinity = generate_vicinity_random(size)
    vicinityValue = val(size, vicinity, flow, distance)
    vicinityValueOLD = vicinityValue
    print "Cual de las siguientes heuristicas quiere probar?"
    print "0) Brute Force"
    print "1) Local Search, random switch"
    print "2) Local Search, next switch"
    num = ''
    while True:
        try:
            num = int(raw_input("Seleccione uno: "))
            if int(num) in [0, 1, 2]:
                break
        except:
            print 'Por favor un numero'

    options = {
        0: obtain_min_force,
        1: obtain_min_random,
        2: obtain_min_random_next,
    }
    print "Empezamos con valor: ", vicinityValueOLD
    options[num](vicinity, vicinityValue, size, flow, distance, maxtime)


if __name__ == "__main__":
    main(sys.argv)
