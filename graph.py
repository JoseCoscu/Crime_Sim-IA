import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import random
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
    """
    Encuentra el camino más corto entre el nodo inicial y el nodo objetivo en un grafo utilizando el algoritmo A*.

    Parameters:
        grafo (nx.Graph): El grafo en el que se realiza la búsqueda.
        nodo_inicial: El nodo inicial.
        nodo_objetivo: El nodo objetivo.

    Returns:
        list: El camino más corto desde el nodo inicial hasta el nodo objetivo.
    """
    lista_abierta = [(0, nodo_inicial)]  # Tuplas de la forma (f, nodo)
    heapq.heapify(lista_abierta)
    padres = {}
    g_score = {nodo_inicial: 0}

    while lista_abierta:
        _, nodo_actual = heapq.heappop(lista_abierta)

        if nodo_actual == nodo_objetivo:
            camino = [nodo_objetivo]
            while nodo_actual != nodo_inicial:
                nodo_actual = padres[nodo_actual]
                camino.append(nodo_actual)
            camino.reverse()
            return camino

        for vecino in grafo.neighbors(nodo_actual):
            g_temp = g_score[nodo_actual] + grafo[nodo_actual][vecino]['weight']
            if vecino not in g_score or g_temp < g_score[vecino]:
                g_score[vecino] = g_temp
                f_score = g_temp + calcular_costo_camino([vecino, nodo_objetivo],
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


def generar_grafo_aleatorio_con_pesos(num_nodos, probabilidad_conexion, max_coord):
    """
    Genera un grafo aleatorio con el número de nodos especificado y una probabilidad
    de conexión entre pares de nodos. Asigna pesos a las aristas basados en la distancia euclidiana.

    Parameters:
        num_nodos (int): Número de nodos en el grafo.
        probabilidad_conexion (float): Probabilidad de conexión entre dos nodos.
        max_coord (int): Máximo valor para las coordenadas de los nodos.

    Returns:
        nx.Graph: El grafo generado.
    """
    G = nx.Graph()
    nodos = list(range(1, num_nodos + 1))

    # Generar coordenadas aleatorias para los nodos
    coordenadas = {nodo: (random.randint(0, max_coord), random.randint(0, max_coord)) for nodo in nodos}
    G.add_nodes_from(nodos)

    # Generar aristas aleatorias y asignar pesos basados en la distancia euclidiana
    for nodo1 in range(1, num_nodos + 1):
        for nodo2 in range(nodo1 + 1, num_nodos + 1):
            if random.random() < probabilidad_conexion:
                peso = distancia_euclidiana(coordenadas[nodo1], coordenadas[nodo2])
                G.add_edge(nodo1, nodo2, weight=peso)

    return G


# Ejemplo de uso
graph = generar_grafo_aleatorio_con_pesos(10, 0.5, 8)
print("Nodos del grafo:", graph.nodes())
print("Aristas del grafo con pesos:", graph.edges(data=True))



camino_mas_corto = a_estrella(graph, 1, 10)

print("Camino más corto:", camino_mas_corto)


# Visualizar el grafo con etiquetas de peso redondeadas a 2 lugares decimales en las aristas
pos = nx.spring_layout(graph)  # Posiciones de los nodos para la visualización
nx.draw(graph, pos, with_labels=True)  # Dibuja el grafo con nodos etiquetados
labels = {(u, v): f"{weight:.2f}" for u, v, weight in graph.edges(data='weight')}  # Redondea los pesos a 2 lugares decimales
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)  # Etiqueta las aristas con los pesos redondeados
plt.show()

