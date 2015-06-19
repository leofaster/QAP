#! /usr/bin/python
import sys
import random
import time
from itertools import permutations
from math import factorial


# FUNCIONES CORE

# GENERAMOS LA PRIMERA SOLUCION DE FORMA RANDOM
def generate_first_solution_random(size):
    v = list(set(range(0, size)))
    for i in range(size):
        rand = random.choice(v)
        v.remove(rand)
        v.append(rand)

    return v


# Evaluamos un vector
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
# FIN FUNCIONES CORE


def valGreedy(size, flow, distance):
    values = []
    for i in range(size):
        for j in range(size):
            if i == j:
                pass
            else:
                values.append(
                    (
                        int(flow[i][j]) * int(distance[i][j]),
                        (i, j)
                    )
                )
    values.sort()
    return values


# OPERADORES DE VECINDAD

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

# FIN OPERADORES DE VECINDAD


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


def ILS(vector, vectorValue, size, flow, distance, maxtime, fi):
    max_iterations = factorial(size)
    laps = 0
    newVector = vector[:]
    newValue = vectorValue
    min_local_counter = 0
    start_time = time.time()

    while laps < max_iterations and min_local_counter < 500:
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

    # print "Vector inicial: ", vector
    # print "Vector final", newVector
    # print "Empezamos con valor: ", vectorValue
    # print "Mejor valor: ", newValue
    # print "Tiempo de corrida: %s" % (time.time() - start_time)
    # print "Tiempo de ejecucion: %s" % (time.time() - maxtime)
    # print "Iteraciones: ", laps

    value = "Vector inicial: %s" % vector
    fi.write(str(value)+'\n')
    value = "Vector final: %s" % newVector
    fi.write(str(value)+'\n')
    value = "Empezamos con valor: %s" % vectorValue
    fi.write(str(value)+'\n')
    value = "Mejor valor: %s" % newValue
    fi.write(str(value)+'\n')
    value = "Tiempo de corrida: %s" % (time.time() - start_time)
    fi.write(str(value)+'\n')
    value = "Tiempo de ejecucion: %s" % (time.time() - maxtime)
    fi.write(str(value)+'\n')
    value = "Iteraciones: %s" % laps
    fi.write(str(value)+'\n')





def VNS(vector, vectorValue, size, flow, distance, maxtime, fi):
    max_iterations = factorial(size)
    laps = 0
    newVector = vector[:]
    newValue = vectorValue
    min_local_counter = 0
    start_time = time.time()
    k = 1
    while laps < max_iterations and min_local_counter < 500:
        k = 1
        while k < 4:
            laps += 1
            sol_inicial_per = pertubation_ils(newVector[:])
            val_sol_inic_per = val(size, sol_inicial_per, flow, distance)
            min_local_sol_inicial, min_loca_value_value = localSearch(
                sol_inicial_per[:],
                newValue,
                size,
                flow,
                distance,
                maxtime,
                k
            )
            if min_loca_value_value < val_sol_inic_per:
                newVector = min_local_sol_inicial
                newValue = min_loca_value_value
                min_local_counter = 1
                k = 1
                print "Mejora"
            else:
                k += 1
                min_local_counter += 1

    # print "Vector inicial: ", vector
    # print "Vector final", newVector
    # print "Empezamos con valor: ", vectorValue
    # print "Mejor valor: ", newValue
    # print "Tiempo de corrida: %s" % (time.time() - start_time)
    # print "Tiempo de ejecucion: %s" % (time.time() - maxtime)
    # print "Iteraciones: ", laps

    value = "Vector inicial: %s" % vector
    s = str(value + '\n')
    fi.write(s)
    value = "Vector final: %s" % newVector
    s = str(value + '\n')
    fi.write(s)
    value = "Empezamos con valor: %s" % vectorValue
    s = str(value + '\n')
    fi.write(s)
    value = "Mejor valor: %s" % newValue
    s = str(value + '\n')
    fi.write(s)
    value = "Tiempo de corrida: %s" % (time.time() - start_time)
    s = str(value + '\n')
    fi.write(s)
    value = "Tiempo de ejecucion: %s" % (time.time() - maxtime)
    s = str(value + '\n')
    fi.write(s)
    value = "Iteraciones: %s" % laps
    s = str(value + '\n')
    fi.write(s)


def generate_vector_greedy(size, flow, distance):
    values = valGreedy(size, flow, distance)
    primera_solucion = []
    for val in values[:size]:
        par = random.choice(values[:size])
        values.remove(par)
        primera_solucion.append(par[1])
    vector_solucion = [0 for x in range(size)]
    vector_x = []
    vector_y = []
    for val in primera_solucion:
        vector_x.append(val[0])
        vector_y.append(val[1])

    while vector_x:
        if vector_solucion[vector_x[0]] == 0:
            tmp = vector_y[0]
            vector_solucion[vector_x[0]] = tmp
            vector_x.remove(vector_x[0])
            vector_y.remove(vector_y[0])
            while vector_y.count(tmp) > 0:
                index = vector_y.index(tmp)
                vector_y.pop(index)
                vector_x.pop(index)
        else:
            vector_x.remove(vector_x[0])
            vector_y.remove(vector_y[0])

    resto = list(set(range(size)) - set(vector_solucion))
    while resto:
        val = random.choice(resto)
        # print vector_solucion
        vector_solucion[vector_solucion.index(0)] = val
        resto.remove(val)

    return vector_solucion


def GRASP(vector, vectorValue, size, flow, distance, maxtime, fi):
    max_iterations = factorial(size)
    laps = 0
    newVector = generate_vector_greedy(size, flow, distance)
    newValue = val(size, newVector, flow, distance)
    min_local_counter = 0
    start_time = time.time()

    while laps < max_iterations and min_local_counter < 500:
        min_local, min_loca_value_value = localSearch(
            newVector[:],
            newValue,
            size,
            flow,
            distance,
            maxtime,
            1
        )
        greydy_vec = generate_vector_greedy(size, flow, distance)
        greedy_val = val(size, greydy_vec, flow, distance)

        tuple_greedy = (greedy_val, greydy_vec)
        tuple_LS = (min_loca_value_value, min_local)
        min_par = min(tuple_greedy, tuple_LS)

        if newValue > min_par[0]:
            newValue = min_par[0]
            newVector = min_par[1]
            print "MEJORA"
            min_local_counter = 1
        else:
            min_local_counter += 1
        laps += 1

    # print "Vector inicial: ", vector
    # print "Vector final", newVector
    # print "Empezamos con valor: ", vectorValue
    # print "Mejor valor: ", newValue
    # print "Tiempo de corrida: %s" % (time.time() - start_time)
    # print "Tiempo de ejecucion: %s" % (time.time() - maxtime)
    # print "Iteraciones: ", laps

    value = "Vector inicial: %s" % vector
    s = str(value + '\n')
    fi.write(s)
    value = "Vector final: %s" % newVector
    s = str(value + '\n')
    fi.write(s)
    value = "Empezamos con valor: %s" % vectorValue
    s = str(value + '\n')
    fi.write(s)
    value = "Mejor valor: %s" % newValue
    s = str(value + '\n')
    fi.write(s)
    value = "Tiempo de corrida: %s" % (time.time() - start_time)
    s = str(value + '\n')
    fi.write(s)
    value = "Tiempo de ejecucion: %s" % (time.time() - maxtime)
    s = str(value + '\n')
    fi.write(s)
    value = "Iteraciones: %s" % laps
    s = str(value + '\n')
    fi.write(s)

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
    # MENU seleccionador
    # print "Cual de las siguientes meta-heuristicas quiere probar?"
    # print "0) ILS"
    # print "1) VNS"
    # print "2) GRASP"
    num = 0
    # while True:
        # try:
            # num = int(raw_input("Seleccione uno: "))
            # if int(num) in [0, 1, 2]:
                # break
        # except:
            # print 'Por favor un numero'
    # ValueOLD = first_solutionValue
    pruebas = 100
    options = {
        0: ILS,
        1: VNS,
        2: GRASP,
    }
    fi = open('bur26a.txt', 'w')
    i = 0
    fi.write('Corrida ILS \n')
    while i < pruebas:
        fi.write('\n')

        value = "Corrida # %s" % i
        s = str(value) + '\n'
        fi.write(s)

        first_solution = generate_first_solution_random(size)
        first_solutionValue = val(size, first_solution, flow, distance)
        options[0](
            first_solution[:],
            first_solutionValue,
            size,
            flow,
            distance,
            time.time(),
            fi
        )
        i += 1
    i = 0
    fi.write('\n')
    fi.write('\n')
    fi.write('Corrida VNS \n')

    while i < pruebas:
        fi.write('\n')
        value = "Corrida # %s" % i
        s = str(value) + '\n'
        fi.write(s)

        first_solution = generate_first_solution_random(size)
        first_solutionValue = val(size, first_solution, flow, distance)
        options[1](
            first_solution[:],
            first_solutionValue,
            size,
            flow,
            distance,
            time.time(),
            fi
        )
        i += 1
    i = 0
    fi.write('\n')
    fi.write('\n')
    fi.write('Corrida GRASP \n')

    while i < pruebas:
        fi.write('\n')
        value = "Corrida # %s" % i
        s = str(value) + '\n'
        fi.write(s)

        first_solution = generate_first_solution_random(size)
        first_solutionValue = val(size, first_solution, flow, distance)
        options[2](
            first_solution[:],
            first_solutionValue,
            size,
            flow,
            distance,
            time.time(),
            fi
        )
        i += 1

    fi.close()


if __name__ == "__main__":
    main(sys.argv)
