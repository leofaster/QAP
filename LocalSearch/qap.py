#! /usr/bin/python
import sys
import random
import time, timing
import itertools
from math import factorial


def val(size, vector, flow, distance):
    value = 0
    for i in range(size):
        for j in range(size):
            # print i, j
            value += int(flow[i][j]) * int(distance[vector[i]][vector[j]])

    return value


def swap_positions(vector, first, second):
    temp = vector[first]
    vector[first] = vector[second]
    vector[second] = temp

    return vector


# Se evalua el vector solucion y se le aplica el operador de vecindad.
# Se guarda la vecindad en una lista de pares.
def operator1_vecinity(value, vector, size, flow, distance):
    lista = []
    lista.append((value, vector))
    for i, k in enumerate(vector):
        tmp = []
        if (i+1 < len(vector)):
            tmp = swap_positions(vector, i, i+1)
        else:
            tmp = swap_positions(vector, i, 0)
        lista.append(
            (
                val(
                    size=size,
                    vector=tmp,
                    flow=flow,
                    distance=distance
                ),
                tmp
            )
        )
    return lista




def generate_first_solution_random(size):
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


def obtain_min_random(vector, vectorValue, size, flow, distance, maxtime):
    maxlaps = factorial(size)
    laps = 0
    newVector = vector
    newValue = vectorValue
    timming.start()
    while laps < maxlaps:
        lista = operator1_vecinity(
            value=newValue,
            vector=newVector,
            size=size,
            flow=flow,
            distance=distance
        )
        newValue = min(lista)[0]
        newVector = min(lista)[1]



    # position = 0
    # laps = 0
    # while time.clock() < maxtime:
    #     laps += 1
    #     newvector = permute_min_local_random(vector, position)
    #     newvectorValue = val(size, newvector, flow, distance)
    #     if vectorValue > newvectorValue:
    #         vector = newVicinity
    #         vicinityValue = newVicinityValue
    #         position += 1

    print "Mejor valor: ", vicinityValue
    print "Tiempo de corrida: ", 
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

    first_solution = generate_first_solution_random(size)
    first_solutionValue = val(size, first_solution, flow, distance)
    ValueOLD = first_solutionValue
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
        1: obtain_min_random,
        2: obtain_min_random_next,
    }
    print "Empezamos con valor: ", ValueOLD
    options[num](
        first_solution,
        first_solutionValue,
        size,
        flow,
        distance,
        maxtime
    )


if __name__ == "__main__":
    main(sys.argv)
