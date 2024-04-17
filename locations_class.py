# NO  IMPORTAR LA CLASE AGENTE ---->> ERROR DE IMPORTACION CIRCULAR
import networkx as nx
import matplotlib.pyplot as plt
import random as r


class Location:
    def __init__(self, name: str, id: int, cash=100):
        self.name = name
        self.connected_to = {}
        self.people_around = []
        self.id = id
        self.cash = cash
        self.state = {'calm': True, 'rob': False, 'on_fire': False, 'is_open': False, 'investigate': False,
                      "send_car": False,
                      "wait_car": False, 'enabled': True}

    def set_state(self, *args):
        for i in self.state:
            self.state[i] = False
        for i in args:
            self.state[i] = True

    def get_state(self):
        states = []
        for i in self.state.keys():
            if self.state[i]:
                states.append(i)
        return states

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
    def collect():
        pass

class PoliceDepartment(Location):
    def __init__(self, id, name, officers, detectives, cars):
        super().__init__(name, id)
        self.current_officers = officers
        self.current_detectives = detectives
        self.current_cars = cars
        self.jail = []

    def send_patrol(self, location):
        ## Aki solo cambiar el estado de la estacion
        self.state['send_car'] = True
        pol = r.randint(1, len(self.current_officers))
        for i in range(pol):
            pol_ran = r.choice(self.current_officers)
            pol_ran.set_state('work', 'go_to_rob')
            pol_ran.call_of_dutty(location)
    def collect(self,officer):
        officer.home.cash += 100
        return

        

class FireDepartment(Location):
    def __init__(self, id, name, fire_fighters, trucks, water):
        super().__init__(name, id)
        self.fire_fighters = fire_fighters
        self.trucks = trucks
        self.water = water

    def send_fire_truck(self, fire_fighters, truck, water, location):
        return NotImplementedError
    
    def collect(self,fire_man):
        fire_man.home.cash += 100
        return

class Hospital(Location):
    def __init__(self, id, name, ambulances, rooms, doctors):
        super().__init__(name, id)
        self.ambulances = ambulances
        self.rooms = rooms
        self.doctors = doctors
##hacer sistema experto para hospital y cobrar_diagnosticar
##hacer herencia de localidades publicas a hospitales polica y fire_dep

    def send_ambulance(self, place):
        return NotImplementedError
    
    def collect(self,doctor):
        doctor.home.cash += 100
        return


class Store(Location):

    def __init__(self, id, name, stock, staff, cash, product_worth):
        super().__init__(name, id)
        self.staff = staff
        self.cash = cash

    # self.is_open = False Poner esto en los estados del nodo ???????

    def hire(self, people):
        self.staff.append(people)


    def collect(self,store_clerk):
        store_clerk.home.cash += 100
        return
        
class GasStation(Store):

    def __init__(self, id, name, gas, staff, cash):
        super().__init__(id, name, 0, staff, cash, 0)
        self.gas = gas

    def restock_gas(self):
        self.gas = 100


class House(Location):
    def __init__(self, id, name):
        super().__init__(name, id)


class Bank(Location):
    def __init__(self, id, name, staff):
        super().__init__(name, id)
        self.cash = 1000
        self.staff = staff
        self.acount = {}

    def deposit(self, agent, amount):
        if agent.id in self.acount:
            self.acount[agent.id] += amount
        else:
            self.acount[agent.id] = amount
        agent.cash -= amount
        self.cash += amount

    def extract(self, agent, amount):
        if agent.id in self.acount:
            if self.acount[agent.id] >= amount:
                self.acount[agent.id] -= amount
                agent.cash += amount
                self.cash -= amount
    def collect(self,store_clerk):
        store_clerk.home.cash += 100
        return

class Casino(Location):
    def __init__(self, id, name, staff):
        super().__init__(name, id)
        self.cash = 1000000
        self.staff = staff
    
    def collect(self,store_clerk):
        store_clerk.home.cash += 100
        return


def create_map(locations):
    # Crear un grafo
    G = nx.Graph()

    # Agregar nodos al grafo
    for location in locations:
        G.add_node(location.name)

    # Agregar aristas al grafo
    for location in locations:
        for connected_location, dist in location.connected_to.items():
            G.add_edge(location.name, connected_location.name, weight=dist)

    return G


def show_locations(G):
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
