from locations_class import *
import random as r
from graph import a_estrella


class Agent:

    def __init__(self, id, name, location: Location, time, city, all_locations):
        self.id = id
        self.name = name
        self.location = location
        self.location.people_arrived(self)
        self.people_on_sight = location.people_around
        self.cash = 100
        self.time = time
        self.map = city
        self.all_locations = all_locations

    # Para esta funcion faltaria calcular el tiempo que demora dicho movimiento de un lugar a otro basandose en lo
    # implementado en la clase de grafos

    def move_to(self, new_location: Location):
        route = a_estrella(self.map, self.location, new_location)
        route.pop(0)
        path = self.get_places(route)
        for location in path:
            time = self.estimate_arrival_time(location)
            if True: # Condicion seria si ya paso el tiempo
                self.location.people_left(self)
                self.location = location
                self.location.people_arrived(self)
                print(f'{self.name} se movio hacia, {self.location.name}')

    def get_places(self, route):
        path = []
        for i in route:
            for k in self.all_locations:
                if k.name == i:
                    path.append(k)
        return path

    def move_to_random_location(self):
        adjacent_locations = self.location.get_adjacent_locations()
        new_location = r.choice(adjacent_locations)
        self.move_to(new_location)
        # print(f'{self.name} se movio hacia {new_location.name}')

    def get_distance(self, place):
        if place in self.location.connected_to:
            return self.location.connected_to[place]

    def estimate_arrival_time(self, place):
        dist = self.get_distance(place)
        time = 0
        if dist <= 5:
            time = r.randint(3, 5)
        elif 5 < dist < 10:
            time = r.randint(6, 8)
        elif dist >= 10:
            time = r.randint(8, 12)
        return time


class Officer(Agent):
    def __init__(self, id, name, location, weapons, vehicle, mastery, time, city, all_locations):
        super().__init__(id, name, location, time, city, all_locations)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def call_of_dutty(self):
        return NotImplementedError


class Detective(Agent):
    def __init__(self, id, name, location, weapons, vehicle, mastery, time, city, all_locations):
        super().__init__(id, name, location, time, city, all_locations)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def investigate(self):
        return NotImplementedError


class Criminal(Agent):
    def __call__(self, *args, **kwargs):
        self.try_robbery()

    def __init__(self, id, name, location, weapons, vehicle, time, city, all_locations, mastery=1):
        super().__init__(id, name, location, time, city, all_locations)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def calculate_success_probability(self):

        ### Faltaria implementar la comunicacion entre los ladrones para que aumente su prob

        powr = len(str(len(self.people_on_sight) - 1))
        success_probability = self.mastery * (
                1 - ((len(self.people_on_sight) - 1) / 10 ** powr))

        ## Aumentar o disminuir la probabilida del exito dependiendo del lugar
        if isinstance(self.location, House):
            success_probability *= 1.5  # Más fácil robar en una casa
        elif isinstance(self.location, Store):
            success_probability *= 1.2  # Relativamente más fácil robar en una tienda
        elif isinstance(self.location, GasStation):
            success_probability *= 1.2  # Más fácil robar en una gasolinera
        elif isinstance(self.location, PoliceDepartment):
            success_probability *= 0.1  # Muy dificil robar en la estacion de Policia
        elif isinstance(self.location, Hospital):  # No hay necesidad de robar en el Hospital
            success_probability *= 0
        elif isinstance(self.location, Bank) or isinstance(self.location, Casino):
            success_probability *= 0.3  # Dificil de robar un banco

        return min(success_probability, 1)  # Asegurarse de que la probabilidad no sea mayor que 1

    def try_robbery(self):

        chances = self.calculate_success_probability()

        if chances >= 0.4:
            is_success = r.random() * (1 + self.mastery / 10)
            if is_success < chances:
                print(f"Robando {self.location.name}")

                stolen_cash = self.location.cash / 10 * self.mastery
                self.cash += stolen_cash
                self.location.cash -= stolen_cash
                print(f'Dinero robado {stolen_cash} por {self.name}')

                self.mastery += 1
            else:
                print(f'robo fallido en {self.location.name}')
                self.mastery += 0.2
        else:
            print(f'posbilidad de robo muy baja en {self.location.name}')
            self.move_to_random_location()


class Employee(Agent):
    ## Se podria agregar un parametro de percepcion para que un empleado pueda adelantarse a un robo

    def __init__(self, id, name, location, work_place: Location, time, city, all_locations):
        super().__init__(id, name, location, time, city, all_locations)
        self.hired_in = work_place

    def go_work(self):
        self.move_to(self.hired_in)


class Citizen(Agent):
    def __call__(self, *args, **kwargs):
        self.move_to_random_location()

    def __init__(self, id, name, location, time, city, all_locations):
        super().__init__(id, name, location, time, city, all_locations)