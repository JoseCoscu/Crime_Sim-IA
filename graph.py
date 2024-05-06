import networkx as nx

import math
import heapq


def calcular_costo_camino(camino, grafo):
    """
    Calcula el costo total de un camino en un grafo.

    Parameters:
        camino (list): Lista de nodos en el camino.
        grafo (nx.Graph): El grafo en el que se encuentra el camino.

    Returns:
        float: El costo total del camino.
    """
    costo_total = 0
    for i in range(len(camino) - 1):
        try:
            costo_total += grafo[camino[i]][camino[i + 1]]['weight']
        except:
            continue
    return costo_total


def a_estrella(grafo, nodo_inicial, nodo_objetivo):
    lista_abierta = [(0, nodo_inicial.name)]
    heapq.heapify(lista_abierta)
    padres = {}
    g_score = {nodo_inicial.name: 0}

    while lista_abierta:
        _, nodo_actual = heapq.heappop(lista_abierta)

        if nodo_actual == nodo_objetivo.name:
            camino = [nodo_objetivo.name]
            while nodo_actual != nodo_inicial.name:
                nodo_actual = padres[nodo_actual]
                camino.append(nodo_actual)
            camino.reverse()
            return camino

        for vecino in grafo.neighbors(nodo_actual):
            g_temp = g_score[nodo_actual] + grafo[nodo_actual][vecino]['weight']
            if vecino not in g_score or g_temp < g_score[vecino]:
                g_score[vecino] = g_temp
                f_score = g_temp + calcular_costo_camino([vecino, nodo_objetivo.name],
                                                         grafo)  # Heurística: distancia al objetivo
                heapq.heappush(lista_abierta, (f_score, vecino))
                padres[vecino] = nodo_actual

    return None  # No se encontró un camino


def distancia_euclidiana(coord1, coord2):
    """
    Calcula la distancia euclidiana entre dos puntos en un espacio euclidiano.

    Parameters:
        coord1 (tuple): Coordenadas del primer punto (x, y).
        coord2 (tuple): Coordenadas del segundo punto (x, y).

    Returns:
        float: La distancia euclidiana entre los dos puntos.
    """
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

