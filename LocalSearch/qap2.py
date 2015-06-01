#! /usr/bin/python
import sys
import random
import time
from itertools import permutations
from math import factorial


def val(size, vector, flow, distance):
    value = 0
    for i in range(size):
        for j in range(size):
            # print i, j
            value += int(flow[i][j]) * int(distance[vector[i]][vector[j]])

    return value


def swap_positions(vector, first, second):
    newVector = vector
    temp = newVector[first]
    newVector[first] = newVector[second]
    newVector[second] = temp
    return newVector


# Se evalua el vector solucion y se le aplica el operador de vecindad.
# Se guarda la vecindad en una lista de pares.
# Se trabaja con el operador de swap inmediatamente nexto
def operator_vecinity1(value, vector, size, flow, distance):
    lista = []
    newVector = vector
    lista.append((value, newVector))
    for i, k in enumerate(vector):
        result = []
        if (i + 1 < len(vector)):
            result = swap_positions(vector[:], i, i + 1)
        else:
            result = swap_positions(vector[:], i, 0)
        tupla = (
            val(
                size=size,
                vector=result,
                flow=flow,
                distance=distance
            ),
            result
        )
        lista.append(
            (
                tupla
            )
        )
    return lista


# Segundo operador de vecindad. Swap con uno de por medio
def operator_vecinity2(value, vector, size, flow, distance):
    lista = []
    newVector = vector
    lista.append((value, newVector))
    for i, k in enumerate(vector):
        result = []
        if (i + 2 < len(vector)):
            result = swap_positions(vector[:], i, i + 2)
        else:
            result = swap_positions(vector[:], i, i - 2)
        tupla = (
            val(
                size=size,
                vector=result,
                flow=flow,
                distance=distance
            ),
            result
        )
        lista.append(
            (
                tupla
            )
        )
    return lista


# Tercero operador de vecindad. Swap con dos de por medio
def operator_vecinity3(value, vector, size, flow, distance):
    lista = []
    newVector = vector
    lista.append((value, newVector))
    for i, k in enumerate(vector):
        result = []
        if (i + 3 < len(vector)):
            result = swap_positions(vector[:], i, i + 3)
        else:
            result = swap_positions(vector[:], i, i - 3)
        tupla = (
            val(
                size=size,
                vector=result,
                flow=flow,
                distance=distance
            ),
            result
        )
        lista.append(
            (
                tupla
            )
        )
    return lista


# GENERAMOS LA PRIMERA SOLUCION DE FORMA RANDOM
def generate_first_solution_random(size):
    v = list(set(range(0, size)))
    for i in range(size):
        rand = random.choice(v)
        v.remove(rand)
        v.append(rand)

    return v


def localSearch(vector, vectorValue, size, flow, distance, maxtime, operator):
    # Diccionario que permite cambiar rapidamente el operador que queremos usar.
    operators = {
        1: operator_vecinity1,
        2: operator_vecinity2,
        3: operator_vecinity3,
    }
    maxlaps = factorial(size)
    laps = 0
    min_local_counter = 0
    mejoras = 0
    newVector = vector[:]
    newValue = vectorValue
    # start_time = time.time()
    while laps < maxlaps and min_local_counter < 2:
        lista = operators[operator](
            value=newValue,
            vector=newVector[:],
            size=size,
            flow=flow,
            distance=distance
        )
        tmp0 = min(lista)[0]
        tmp1 = min(lista)[1]
        if newValue >= tmp0:
            if newValue == tmp0:
                min_local_counter += 1
            else:
                mejoras += 1
                newValue = tmp0
                newVector = tmp1
                min_local_counter = 0

        laps += 1
    # print "Vector inicial: ", vector
    # print "Vector final", newVector
    # print "Empezamos con valor: ", vectorValue
    # print "Mejor valor: ", newValue
    # print "Tiempo de corrida: %s" % (time.time() - start_time)
    # print "Iteraciones: ", laps
    return newVector, newValue


def pertubation_ils(vector):
    if len(vector) > 4:
        middle = len(vector)/2
        up = middle + 1
        down = middle - 1
        tmp = vector[down]
        vector[down] = vector[up]
        vector[up] = vector[len(vector)-1]
        vector[len(vector)-1] = vector[middle]
        vector[middle] = vector[0]
        vector[0] = tmp

    else:
        tmp = vector[1]
        vector[1] = vector[0]
        vector[0] = tmp

    return vector


def ILS(vector, vectorValue, size, flow, distance, maxtime):
    max_iterations = factorial(size)
    laps = 0
    newVector = vector[:]
    newValue = vectorValue
    min_local_counter = 0
    start_time = time.time()

    while laps < max_iterations and min_local_counter < 5000:
        min_local, min_loca_value_value = localSearch(
            newVector[:],
            newValue,
            size,
            flow,
            distance,
            maxtime,
            1
        )
        laps += 1
        pertubed_vector = []
        new_min_local = []
        new_min_value = 0
        if min_local_counter % 10 == 0:
            pertubed_vector = generate_first_solution_random(size)
            new_min_local, new_min_value = localSearch(
                pertubed_vector[:],
                newValue,
                size,
                flow,
                distance,
                maxtime,
                2
            )
        else:
            pertubed_vector = pertubation_ils(min_local[:])
            new_min_local, new_min_value = localSearch(
                pertubed_vector[:],
                newValue,
                size,
                flow,
                distance,
                maxtime,
                3
            )
        # print min_loca_value_value > new_min_value
        new_local = min(
            (new_min_value, new_min_local),
            (min_loca_value_value, min_local)
        )
        if newValue > new_local[0]:
            newVector = new_local[1]
            newValue = new_local[0]
            print "MEJORA"
            min_local_counter = 1

        else:
            min_local_counter += 1
            # print "parao"


    print "Vector inicial: ", vector
    print "Vector final", newVector
    print "Empezamos con valor: ", vectorValue
    print "Mejor valor: ", newValue
    print "Tiempo de corrida: %s" % (time.time() - start_time)
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
    print "Cual de las siguientes meta-heuristicas quiere probar?"
    print "0) VNS"
    print "1) GRASP"
    num = ''
    while True:
        try:
            num = int(raw_input("Seleccione uno: "))
            if int(num) in [0, 1, 2]:
                break
        except:
            print 'Por favor un numero'

    options = {
        0: ILS,
        1: ILS,
    }

    options[num](
        first_solution[:],
        first_solutionValue,
        size,
        flow,
        distance,
        maxtime
    )


if __name__ == "__main__":
    main(sys.argv)
