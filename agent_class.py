import time as t
from locations_class import *
import random as r
from graph import a_estrella
from timer import TimeMeter


class Agent:
    def __init__(self, id, name, location: Location, time: TimeMeter, city, all_locations, house: Location):
        self.id = id
        self.name = name
        self.location = location
        self.location.people_arrived(self)
        self.people_on_sight = location.people_around
        self.time = 0
        self.map = city
        self.all_locations = all_locations
        self.sick = {'virus': False, 'inflamacio': False, 'mental': False, 'ninguna': True}
        self.injuries = {'laceracion': False, 'quemadura': False, 'punzon': False, 'golpe': False, 'ninguna': True}
        self.home = house
        self.state = {'move_path': False, 'work': False, 'move_random': False, 'sleep': False, 'in_house': True,
                      'stop_Location': False,
                      'aux_operation': False, 'go_to_rob': False, 'rob_in_progress': False, 'detenido': False,
                      'sick': False,
                      'injure': True}
        self.history = []
        self.locations = {'pd': [], 'hospitals': [], 'stores': [], 'gs_stations': [], 'casinos': [], 'fd': [],
                          'banks': []}

        self.get_locations(all_locations)
        self.time = time

    # Para esta funcion faltaria calcular el tiempo que demora dicho movimiento de un lugar a otro basandose en lo
    # implementado en la clase de grafos

    def get_injuries(self):
        for i in self.injuries.keys():
            if self.injuries[i]:
                return i

    def get_sick(self):
        for i in self.sick.keys():
            if self.sick[i]:
                return i

    def get_locations(self, all_locations):
        for i in all_locations:
            if isinstance(i, PoliceDepartment):
                self.locations['pd'].append(i)
            if isinstance(i, Hospital):
                self.locations['hospitals'].append(i)
            if isinstance(i, Store):
                self.locations['stores'].append(i)
            if isinstance(i, GasStation):
                self.locations['gs_stations'].append(i)
            if isinstance(i, Casino):
                self.locations['casinos'].append(i)
            if isinstance(i, FireDepartment):
                self.locations['fd'].append(i)
            if isinstance(i, Bank):
                self.locations['banks'].append(i)

    def get_police_departments(self):
        places = []
        for i in self.all_locations:
            if isinstance(i, PoliceDepartment):
                places.append(i)

    def go_bank_deposit(self):
        if 'go_deposit' not in self.home.get_state():
            self.home.state['go_deposit'] = True
            bank = self.nearest_place(self.locations['banks'][0])
            self.move_to(bank)
            self.stay_in_place(2)
            if self.home.cash > 100:
                bank.deposit(self, self.home.cash - 100)
                self.home.state['go_deposit'] = False
                print(f'{self.name} deposito en el banco {bank.name}')
                print(f'dinero en la casa de {self.name} es : {self.home.cash}')

    def go_bank_extract(self):
        if 'go_deposit' not in self.home.get_state():
            self.home.state['go_extract'] = True
            bank = self.nearest_place(self.locations['banks'][0])
            self.move_to(bank)
            self.stay_in_place(2)
            if self.home.cash < 100:
                bank.extract(self, abs(self.home.cash - 100))
                self.home.state['go_extract'] = False
                print(f'{self.name} deposito en el banco {bank.name}')
                print(f'dinero en la casa de {self.name} es : {self.home.cash}')

    def stay_in_place(self, time):
        start_time = self.time.get_global_time()
        while True:
            elapse_time = self.time.get_global_time() - start_time
            if elapse_time >= time:
                break

    def get_total_distance(self, route):
        dist = 0
        for i in range(len(route) - 1):
            dist += route[i].connected_to[route[i + 1]]
        return dist

    def get_state(self):
        states = []
        for i in self.state.keys():
            if self.state[i]:
                states.append(i)
        return states

    def set_state(self, *args):
        for i in self.state:
            self.state[i] = False
        for i in args:
            self.state[i] = True

    def go_home(self):
        self.move_to(self.home)

    def go_to_hospital(self):
        hospital = self.nearest_place(self.locations['hospitals'][0])
        self.move_to(hospital)
        stay, time_local, medication = hospital.diagnostic(self.get_injuries(), self.get_sick())
        if stay:
            self.stay_in_place(time_local)
            if (medication != ""):
                print(f"{self.name} se recupero de {self.get_sick()} - {self.get_injuries()} y tomando {medication}")
            else:
                print(f"{self.name} se recupero de {self.get_sick()} y tomando {medication}")
            self.sick = {k: False if v else v for k, v in self.sick.items()}
            self.injuries = {k: False if v else v for k, v in self.injuries.items()}
            self.injuries['ninguna'] = True
            self.sick['ninguna'] = True

            self.go_home()
        else:
            self.go_home()
            self.stay_in_place(time_local)
            self.injuries['ninguna'] = True
            self.sick['ninguna'] = True
            print(f"{self.name} se recupero de {self.get_sick()} tomando {medication}")
            self.sick = {k: False if v else v for k, v in self.sick.items()}
            self.injuries = {k: False if v else v for k, v in self.injuries.items()}

    def move_to(self, new_location: Location):
        route = a_estrella(self.map, self.location, new_location)
        route.pop(0)
        path = self.get_places(route)
        for location in path:
            start_time = self.time.get_global_time()
            times = self.estimate_arrival_time(location)
            while True:
                end_time = self.time.get_global_time()  # Registro del tiempo de finalización
                elapsed_time = end_time - start_time  # Cálculo del tiempo transcurrido
                if elapsed_time >= times:  # Condicion seria si ya paso el tiempo
                    previus_location = self.location
                    self.location.people_left(self)
                    self.location = location
                    self.location.people_arrived(self)
                    print(
                        f'{self.name} se movio hacia, {self.location.name} y en el {self.time.get_global_time()} segundo desde {previus_location.name}\n')
                    break
            if "rob" in self.location.get_state() and not (isinstance(self, Criminal)):
                if isinstance(self, Officer or Detective):
                    print(
                        'Policia o Detective apresa al ladron')  # si un oficial o un detective llega aun lugar y estan robando
                    # break
                else:
                    station_pol = self.nearest_place(self.locations['pd'][0])
                    print(f"Calling nearest Police Station en {self.time.get_global_time()} segundos por {self.name}\n")
                    station_pol.send_patrol()
                    self.location.state['calm'] = False
                    self.location.state['wait_car'] = True
                    # print(station_pol.get_state())
                    break

    def nearest_place(self, place):
        type_of = type(place)
        nearest_place = None
        dist = 999999
        for i in self.all_locations:
            if isinstance(i, type_of):
                path = a_estrella(self.map, self.location, i)
                path.pop(0)
                route = self.get_places(path)
                place_dist = self.get_total_distance(route)
                if place_dist < dist:
                    nearest_place = i
                    dist = place_dist
        return nearest_place

    def move_to_random_location(self):
        new_location = r.choice(self.all_locations)
        print(f"{self.name} se va a mover de {self.location.name} a {new_location.name}")
        self.move_to(new_location)

    def get_places(self, route):
        path = []
        for i in route:
            for k in self.all_locations:
                if k.name == i:
                    path.append(k)
        return path

    def get_distance(self, place):
        if place in self.location.connected_to:
            return self.location.connected_to[place]

    def estimate_arrival_time(self, place):
        dist = self.get_distance(place)
        return dist
    
    def go_to_store(self):
        store = self.nearest_place(self.locations['stores'][0])
        self.move_to(store)
        store.buy(self)
        self.stay_in_place(5)
        self.go_home()

    def go_to_casino(self):
        casino = self.nearest_place(self.locations['casinos'][0])
        self.move_to(casino)
        casino.play(self)
        self.stay_in_place(5)
        self.go_home()
        

class Citizen(Agent):
    def __call__(self, *args, **kwargs):
        while True:
            self.stay_in_place(8)
            if self.get_injuries()!='ninguna' or self.get_sick()!='ninguna':
                self.go_to_hospital()
            if self.home.cash > 100:
                print(f'{self.name} esta depositando')
                self.go_bank_deposit()
            # if self.home.cash < 100:
            #     print(f'{self.name} esta extrayendo')
            #     self.go_bank_extract()
            if self.time.get_global_time() >= 22:
                print(f'{self.name} esta regresando a su casa')
            aux_mov=r.random()
            if aux_mov<0.5:
                print("########move random")
                self.move_to_random_location()
            elif aux_mov<0.8 and aux_mov>=0.5:
                print("########move casino")    
                self.go_to_casino()
            else:
                print("########move store")    
                self.go_to_store()
            if self.time.get_global_time() >= 100:
                self.go_home()


    def __init__(self, id, name, location, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)


class Officer(Citizen):
    def __init__(self, id, name, location, weapons, vehicle, mastery, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery


    def __call__(self, *args, **kwargs):
        start_time = self.time.get_global_time()
        while True:
            aux_loc = None
            if 'go_to_rob' in self.get_state():
                for i in self.all_locations:
                    if 'wait_car' in i.get_state():
                        aux_loc = i
                        break
            if aux_loc:
                self.call_of_dutty(aux_loc)
                break

    def call_of_dutty(self, location, criminal=None):
        print(f'Atendiendo crimen en {self.time.get_global_time()}')
        if 'work' in self.get_state():  # quitar
            self.move_to(location)
            if criminal and criminal in location.people_around:
                print(f'apresar a {criminal.name}')
            people_in_rob = [x for x in location.people_around if 'rob_in_progress' in x.get_state()]
            if people_in_rob:
                for i in people_in_rob:
                    chance = self.criminal_chance(i)
                    if chance and not i.state['detenido']:

                        i.state['detenido'] = True
                        i.state['rob_in_progress'] = False
                        print(f'{self.name} atrapo a {i.name} en {self.time.get_global_time()} segundos\n')
                    elif not chance:
                        print(f'{i.name} escapo')


    def criminal_chance(self, criminal):
        # chance_c = criminal.mastery / 10
        # chance_o = self.mastery / 10
        # if chance_o >= chance_c:
        #     is_success = r.random() - chance_c
        #     if is_success >= 0.5:
        #         return True
        #     else:
        #         return False
        # else:
        #     is_success = r.random() - chance_c
        #     if is_success >= 0.5:
        #         return False
        return True


class Detective(Citizen):
    def __init__(self, id, name, location, weapons, mastery, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.weapons = weapons
        self.mastery = mastery

    def investigate(self):
        return NotImplementedError


class Employee(Citizen):
    ##Se podria agregar un parametro de percepcion para que un empleado pueda adelantarse a un robo
    def __call__(self, *args, **kwargs):
        aux_random=r.random()
        print(aux_random)
        if aux_random<0.85:
            self.go_work()
        else:
            aux_random2=r.randint(0,len(self.sick)-2)
            self.sick['ninguna']=False
            self.sick[list(self.sick.keys())[aux_random2]]=True
            self.go_to_hospital()

    def __init__(self, id, name, location, work_place: Location, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.hired_in = work_place
        self.hired_in.staff.append(self)
        self.route= self.get_route()
        self.walk_time= self.get_total_distance(self.route)

    def get_route(self):
        route= a_estrella(self.map, self.location, self.hired_in)
        return self.get_places(route)
    
    def go_work(self):
        self.stay_in_place(20-self.walk_time)
        self.move_to(self.hired_in)
        print('llego a trabajar')
        self.stay_in_place(50)
        print('termino de trabajar')
        self.home.collect()
        self.go_home()
##no borrar


class Criminal(Agent):
    def __call__(self, *args, **kwargs):
        while True:
            self.move_to_random_location()
            if isinstance(self.location, PoliceDepartment):
                continue
            if isinstance(self.location, FireDepartment):
                continue
            if isinstance(self.location, Hospital):
                continue
            self.try_robbery()

    def __init__(self, id, name, location, weapons, vehicle, time, city, all_locations, house, mastery=1):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def calculate_rob_time(self):
        rob_time = 100
        ## Aumentar o disminuir el tiempo del robo dependiendo del lugar
        if isinstance(self.location, House):
            rob_time *= 0.2  # Más fácil robar en una casa
        elif isinstance(self.location, Store) or isinstance(self.location, GasStation):
            rob_time *= 0.3  # Relativamente más fácil robar en una tienda
        elif isinstance(self.location, PoliceDepartment):
            rob_time *= 3  # Muy dificil robar en la estacion de Policia
        elif isinstance(self.location, Bank) or isinstance(self.location, Casino):
            rob_time *= 2  # Dificil de robar un banco o Casono

        return rob_time

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
        if self.location == self.home:
            self.move_to_random_location()
            return
        chances = self.calculate_success_probability()
        rob_time = self.calculate_rob_time()  ## Arreglar tiempo de robo
        if chances >= 0.4 and 'calm' in self.location.get_state():
            start_time = self.time.get_global_time()
            self.state['rob_in_progress'] = True
            self.location.state['calm'] = False
            self.location.state['rob'] = True
            is_success = r.random() * (1 + self.mastery / 10)
            print(f"Robando {self.location.name} por {self.name}\n")
            hurt_someone = r.random()
            while True:
                end_time = self.time.get_global_time()
                elapse_time = end_time - start_time
                if elapse_time >= rob_time:
                    if hurt_someone >= 0.1:  ## Modificar esta probabilidad luego
                        person = r.choice(self.people_on_sight)
                        print(f'Se le va a meter la tiza a {person.name}')
                        if person == self:
                            break
                        injure = r.choice(list(self.injuries.keys()))
                        person.injuries[injure] = True
                        person.injuries['ninguna'] = False
                        # print(person.get_injuries())
                    break
            if 'detenido' in self.get_state():
                print(f'{self.name} ha sido apresado\n')
                return

            if is_success < chances:
                stolen_cash = self.location.cash / 10 * self.mastery
                self.home.cash += stolen_cash
                self.location.cash -= stolen_cash
                print(f'Dinero robado {stolen_cash} por {self.name}')
                self.mastery += 1
            else:
                print(f'robo fallido en {self.location.name} en {self.time.get_global_time()} segundos\n')
                self.mastery += 0.2
        else:
            print(f'posbilidad de robo muy baja en {self.location.name}\n')
            self.move_to(self.all_locations[r.randint(0, 10)])

        # self.move_to(self.all_locations[r.randint(0, 10)])
