#! /usr/bin/python
import sys
import random
import time
from itertools import permutations, groupby
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

# OPERADORES DE POBLACION

def operador_voto1(padre1, padre2):
    hijo = []
    padre22 = padre2[:]
    padre12 = padre1[:]
    selector = True
    while padre12:
        if selector:
            elem = padre12.pop(0)
            padre22.remove(elem)
            hijo.append(elem)
            selector = False
        else:
            elem = padre22.pop(0)
            padre12.remove(elem)
            hijo.append(elem)
            selector = True
    return hijo


def operador_voto2(padre1, padre2):
    hijo = []
    padre22 = padre1[:]
    padre12 = padre2[:]
    selector = True
    while padre12:
        if selector:
            elem = padre12.pop(0)
            padre22.remove(elem)
            hijo.append(elem)
            selector = False
        else:
            elem = padre22.pop(0)
            padre12.remove(elem)
            hijo.append(elem)
            selector = True
    return hijo


# FIN OPERADORES DE POBLACION

# ELEGIR MEJORES PADRES RANDOM
def random_padres(sumtotal):
    rand1 = random.randint(0, sumtotal)
    rand2 = random.randint(0, sumtotal)
    while rand1 == rand2:
        rand2 = random.randint(0, sumtotal)
    return rand1, rand2
# FIN ELEGIR MEJORES PADRES RANDOM




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


def generador_poblacional_random(size, sizevalue):
    soluciones = []
    i = 0
    while i < sizevalue:
        fsolution = generate_first_solution_random(size)
        if fsolution not in soluciones:
            soluciones.append(fsolution)
            i += 1
    return soluciones


def evaluador_poblacional(poblacion, size, flow, distance):
    soluciones = []
    for solucion in poblacion:
        soluciones.append(val(size, solucion, flow, distance))
    return soluciones


def evaluador_fitnes(resultados):
    fitnes = []
    sumatotal = sum(resultados)
    for resultado in resultados:
        fitnes.append(sumatotal/resultado)
    return fitnes, sumatotal


def obtener_index_padre(selector_padre, fitnes):
    index = -1
    acomulado = 0
    for counter, resulado in enumerate(fitnes):
        acomulado += resulado
        if acomulado > selector_padre:
            index = counter
            break
    return index


def eliminar_padres(
    index_padre1,
    index_padre2,
    soluciones,
    resultados,
    fitnes
):
    soluciones.pop(index_padre1)
    soluciones.pop(index_padre2)
    resultados.pop(index_padre1)
    resultados.pop(index_padre2)
    fitnes.pop(index_padre1)
    fitnes.pop(index_padre2)


def eliminar_padres_lista(
    lista_padres,
    soluciones
):
    for padre in lista_padres:
        soluciones.remove(padre)


def agregar_hijos(
    hijo1,
    hijo2,
    soluciones
):
    soluciones.append(hijo1)
    soluciones.append(hijo2)


def agregar_hijos_lista(
    lista_soliciones,
    soluciones
):
    for solucion in lista_soliciones:
        if solucion not in soluciones:
            soluciones.append(solucion)
        # else:
            # soluciones.remove(solucion)


def seleccionador_crianza(
    padre1,
    padre2,
    hijo1,
    hijo2,
    size,
    flow,
    distance
):
    lista = []
    valor_padre1 = val(size, padre1, flow, distance)
    lista.append((valor_padre1, padre1, 'padre'))
    valor_padre2 = val(size, padre2, flow, distance)
    lista.append((valor_padre2, padre2, 'padre'))

    valor_hijo1 = val(size, hijo1, flow, distance)
    lista.append((valor_hijo1, hijo1, 'hijo'))

    valor_hijo2 = val(size, hijo2, flow, distance)
    lista.append((valor_hijo2, hijo2, 'hijo'))
    lista.sort()
    # print lista
    return lista


def ciclo_genetico_con_selector(
    pruebas,
    soluciones,
    size,
    flow,
    distance
):
    ciclo = 0
    resultados = []
    while ciclo < pruebas:
        resultados = evaluador_poblacional(soluciones, size, flow, distance)
        fitnes, sumatotal = evaluador_fitnes(resultados)
        selector_padre1, selector_padre2 = random_padres(sumatotal)
        index_padre1 = obtener_index_padre(selector_padre1, fitnes)
        index_padre2 = obtener_index_padre(selector_padre2, fitnes)
        hijo1 = operador_voto1(
            soluciones[index_padre1],
            soluciones[index_padre2]
        )
        hijo2 = operador_voto2(
            soluciones[index_padre1],
            soluciones[index_padre2]
        )
        criajes = seleccionador_crianza(
            soluciones[index_padre1],
            soluciones[index_padre2],
            hijo1,
            hijo2,
            size,
            flow,
            distance
        )
        delete = 0
        for counter, criaje in enumerate(criajes):
            if criaje[2] == 'hijo':
                if counter < 2:
                    soluciones.append(criaje[1])
                    delete += 1
            if criaje[2] == 'padre':
                if delete > 0:
                    if counter > 1:
                        soluciones.remove(criaje[1])
        ciclo += 1
    return min(resultados)


def ciclo_genetico_sin_selector(
    pruebas,
    soluciones,
    size,
    flow,
    distance
):
    ciclo = 0
    resultados = []
    while ciclo < pruebas:
        resultados = evaluador_poblacional(soluciones, size, flow, distance)
        fitnes, sumatotal = evaluador_fitnes(resultados)
        selector_padre1, selector_padre2 = random_padres(sumatotal)
        index_padre1 = obtener_index_padre(selector_padre1, fitnes)
        index_padre2 = obtener_index_padre(selector_padre2, fitnes)
        hijo1 = operador_voto1(
            soluciones[index_padre1],
            soluciones[index_padre2]
        )
        hijo2 = operador_voto2(
            soluciones[index_padre1],
            soluciones[index_padre2]
        )
        eliminar_padres(
            index_padre1,
            index_padre2,
            soluciones,
            resultados,
            fitnes
        )
        agregar_hijos(hijo1, hijo2, soluciones)
        ciclo += 1
    return min(resultados)


def obtener_datos(f):
    size = int(f.readline().strip())

    f.readline()  # We read and leave this line

    # Initializate the variables
    # vicinity = [0 for x in range(size)]
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
    return matrix, size


def main_genetic(archivo, selector, cantidad, potencia=2):
    f = open(archivo, 'r')
    pruebas = int(cantidad)
    matrix, size = obtener_datos(f)
    f.close()
    flow = matrix[:size]
    distance = matrix[size:]
    # tamano de la poblacion a buscar
    sizevalue = size ** potencia
    soluciones = generador_poblacional_random(size, sizevalue)
    minimo = -1
    if selector == 1:
        minimo = ciclo_genetico_con_selector(
            pruebas,
            soluciones,
            size,
            flow,
            distance
        )
    else:
        minimo = ciclo_genetico_sin_selector(
            pruebas,
            soluciones,
            size,
            flow,
            distance
        )
    print minimo


def main_ss(archivo, iteraciones, potencia=2):
    f = open(archivo, 'r')
    matrix, size = obtener_datos(f)
    flow = matrix[:size]
    distance = matrix[size:]
    # tamano de la poblacion a buscar
    sizevalue = size ** potencia
    # EMPIEZA EL CICLO
    soluciones = generador_poblacional_random(size, sizevalue)
    lista_ss = []
    for solucion in soluciones:
        lista_ss.append(
            (
                val(
                    size,
                    solucion,
                    flow,
                    distance
                ),
                solucion
            )
        )
    lista_ss.sort()
    lista_elite = []
    i = 0
    while i < 5:
        lista_elite.append(lista_ss[i])
        lista_elite.append(
            (
                val(
                    size,
                    lista_ss[i][1][::-1],
                    flow,
                    distance
                ),
                lista_ss[i][1][::-1]
            )
        )
        i += 1
    lista_elite.sort()
    lista_mezcla = []
    p = 0
    while p < iteraciones:
        for e in lista_elite:
            for j in lista_elite[::-1]:
                if e != j:
                    hijo1 = operador_voto1(e[1], j[1])
                    hijo2 = operador_voto2(e[1], j[1])
                    lista_mezcla.append(
                        (
                            val(
                                size,
                                hijo1,
                                flow,
                                distance
                            ),
                            hijo1
                        )
                    )
                    lista_mezcla.append(
                        (
                            val(
                                size,
                                hijo2,
                                flow,
                                distance
                            ),
                            hijo2
                        )
                    )
        lista_mezcla.sort()
        # ELIMINAR DUPLICADOS
        new_lista_mezcla = list(
            lista_mezcla for lista_mezcla,
            _ in groupby(lista_mezcla)
        )
        # ELIMINAR DUPLICADOS
        if new_lista_mezcla[0][0] < lista_elite[-1][0]:
            lista_elite.remove(lista_elite[-1])
            lista_elite.append(new_lista_mezcla[0])
        lista_elite.sort()
        lista_elite = list(
            lista_elite for lista_elite,
            _ in groupby(lista_elite)
        )
        p += 1
    print min(lista_elite)[0]


def main(argv):
    if len(argv) < 2:
        print "USO: archivo [#pruebas d:50] [#potencia d:3] [selector d: 0 - 0 genetico sin selector, 1 genetico con selector, 2 scatter search]"
    else:
        if len(argv) > 1:
            f = sys.argv[1]
        else:
            f = sys.stdin
        if len(argv) > 2:
            pruebas = int(sys.argv[2])
        else:
            pruebas = 50
        if len(argv) > 3:
            potencia = int(sys.argv[3])
        else:
            potencia = 3
        if len(argv) > 4:
            selector = int(sys.argv[4])
        else:
            selector = 0

        options = {
            0: main_genetic,
            1: main_genetic,
        }
        if selector < 2:
            options[selector](
                f,
                selector,
                pruebas,
                potencia
            )
        else:
            main_ss(
                f,
                pruebas,
                potencia
            )
    # matrix, size = obtener_datos(f)
    # flow = matrix[:size]
    # distance = matrix[size:]
    # # tamano de la poblacion a buscar
    # sizevalue = size ** potencia
    # # EMPIEZA EL CICLO
    # soluciones = generador_poblacional_random(size, sizevalue)
    # lista_ss = []
    # for solucion in soluciones:
    #     lista_ss.append(
    #         (
    #             val(
    #                 size,
    #                 solucion,
    #                 flow,
    #                 distance
    #             ),
    #             solucion
    #         )
    #     )
    # lista_ss.sort()
    # lista_elite = []
    # i = 0
    # while i < 5:
    #     lista_elite.append(lista_ss[i])
    #     lista_elite.append(
    #         (
    #             val(
    #                 size,
    #                 lista_ss[i][1][::-1],
    #                 flow,
    #                 distance
    #             ),
    #             lista_ss[i][1][::-1]
    #         )
    #     )
    #     i += 1
    # lista_elite.sort()
    # lista_mezcla = []
    # p = 0
    # while p < pruebas:
    #     for e in lista_elite:
    #         for j in lista_elite[::-1]:
    #             if e != j:
    #                 hijo1 = operador_voto1(e[1], j[1])
    #                 hijo2 = operador_voto2(e[1], j[1])
    #                 lista_mezcla.append(
    #                     (
    #                         val(
    #                             size,
    #                             hijo1,
    #                             flow,
    #                             distance
    #                         ),
    #                         hijo1
    #                     )
    #                 )
    #                 lista_mezcla.append(
    #                     (
    #                         val(
    #                             size,
    #                             hijo2,
    #                             flow,
    #                             distance
    #                         ),
    #                         hijo2
    #                     )
    #                 )
    #     lista_mezcla.sort()
    #     # ELIMINAR DUPLICADOS
    #     new_lista_mezcla = list(
    #         lista_mezcla for lista_mezcla,
    #         _ in groupby(lista_mezcla)
    #     )
    #     # ELIMINAR DUPLICADOS
    #     if new_lista_mezcla[0][0] < lista_elite[-1][0]:
    #         lista_elite.remove(lista_elite[-1])
    #         lista_elite.append(new_lista_mezcla[0])
    #     lista_elite.sort()
    #     lista_elite = list(
    #         lista_elite for lista_elite,
    #         _ in groupby(lista_elite)
    #     )
    #     p += 1
    # print min(lista_elite)[0]

if __name__ == "__main__":
    main(sys.argv)
