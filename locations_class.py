# NO  IMPORTAR LA CLASE AGENTE ---->> ERROR DE IMPORTACION CIRCULAR
import networkx as nx
import matplotlib.pyplot as plt
import random as r


class Location:
    def __init__(self, name: str, id: int):
        self.name = name
        self.connected_to = {}
        self.people_around = []
        self.id = id

    def get_adjacent_locations(self):
        return list(self.connected_to.keys())

    def add_row(self, places, a, b):
        for place in places:
            dist = r.randint(a, b)
            self.connected_to[place] = dist
            place.connected_to[self] = dist

    def people_arrived(self, people):
        self.people_around.append(people)

    def people_left(self, people):
        self.people_around.remove(people)


class PoliceDepartment(Location):
    def __init__(self, id, name, officers, detectives, cars):
        super().__init__(name, id)
        self.current_officers = officers
        self.current_detectives = detectives
        self.current_cars = cars

    def send_patrol(self, cars, place):
        return NotImplementedError


class FireDepartment(Location):
    def __init__(self, id, name, fire_fighters, trucks, water):
        super().__init__(name, id)
        self.fire_fighters = fire_fighters
        self.trucks = trucks
        self.water = water

    def send_fire_truck(self, fire_fighters, truck, water, location):
        return NotImplementedError


class Hospital(Location):
    def __init__(self, id, name, ambulances, rooms, doctors):
        super().__init__(name, id)
        self.ambulances = ambulances
        self.rooms = rooms
        self.doctors = doctors

    def send_ambulance(self, place):
        return NotImplementedError


class Store(Location):

    def __init__(self, id, name, stock, staff, cash, product_worth):
        super().__init__(name, id)
        self.staff = staff
        self.cash = cash
        self.product_w = product_worth
        self.stock = stock

    # self.is_open = False Poner esto en los estados del nodo ???????

    def hire(self, people):
        self.staff.append(people)

    def restock(self):
        self.stock = 100

    def call_police(self):
        return NotImplementedError

    def call_fire_f(self):
        return NotImplementedError


class GasStation(Store):

    def __init__(self, id, name, gas, staff, cash):
        super().__init__(id, name, 0, staff, cash, 0)
        self.gas = gas

    def restock_gas(self):
        self.gas = 100


class Hause(Location):
    def __init__(self, id, name):
        super().__init__(name, id)


class Bank(Location):
    def __init__(self, id, name):
        super().__init__(name, id)


class Casino(Location):
    def __init__(self, id, name):
        super().__init__(name, id)


def show_locations(locations):
    # Crear un grafo
    G = nx.Graph()

    # Agregar nodos al grafo
    for location in locations:
        G.add_node(location.name)

    # Agregar aristas al grafo
    for location in locations:
        for connected_location, dist in location.connected_to.items():
            G.add_edge(location.name, connected_location.name, weight=dist)

    # Diccionario para mapear clases a colores
    color_map = {
        "PNR": "blue",
        "Fire Department": "red",
        "Hospital": "green",
        "House": "cyan",
        "Gas Station": "magenta",
        "Bank": "gold",
        "Store": 'purple',
        'Casino': 'lightgreen'
    }

    # Obtener los colores de los nodos según la clase de lugar
    node_colors = [color_map[location.split('_')[0]] if location.split('_')[0] in color_map else 'gray' for
                   location in G.nodes]

    # Dibujar el grafo con colores en los nodos
    pos = nx.spring_layout(G)  # Calcula las posiciones de los nodos
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=10,
            font_weight="bold", node_color=node_colors)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Agrega etiquetas a las aristas

    # Configuración del gráfico
    plt.title('Conexiones entre lugares')
    plt.axis('off')  # Desactiva los ejes
    plt.show()
