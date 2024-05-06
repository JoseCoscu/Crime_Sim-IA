import time as t
from locations_class import *
import random as r
from graph import a_estrella
from timer import TimeMeter

# from map import indice_criminalidad,indice_agresividad


cant_apresados = 0

cant_rob_report = 0

cant_incendios_att = 0


class Agent:
    def __init__(self, id, name, location: Location, time: TimeMeter, city, all_locations, house: Location):
        self.cant_apresados = 0
        self.cant_rob_report = 0
        self.cant_rob = 0
        self.cant_heridos = 0
        self.cant_incendios = 0
        self.cant_dinero_rob = 0
        self.id = id
        self.name = name
        self.location = location
        self.location.people_arrived(self)
        self.people_on_sight = location.people_around
        self.time = 0
        self.map = city
        self.all_locations = all_locations
        self.sick = {'virus': False, 'inflamacion': False, 'mental': False, 'ninguna': True}
        self.injuries = {'laceracion': False, 'quemadura': False, 'punzon': False, 'golpe': False, 'ninguna': True}
        self.home = house
        self.state = {'move_path': False, 'work': False, 'move_random': False, 'sleep': False, 'in_house': True,
                      'stop_Location': False,
                      'aux_operation': False, 'go_to_rob': False, 'rob_in_progress': False, 'detenido': False,
                      'sick': False,
                      'injure': False, 'on_jail': False}
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
        return 'ninguna'

    def get_sick(self):
        for i in self.sick.keys():
            if self.sick[i]:
                return i
        return 'ninguna'

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
                self.history.append(f'{self.name} deposito en el banco {bank.name} en {self.time.get_global_time()}')
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
        self.history.append(
            f'{self.name}  se va a quedar {self.location.name} por {time} segundos en {self.time.get_global_time()}')
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

            if medication != "":
                print(f"{self.name} se recupero de {self.get_sick()} - {self.get_injuries()} y tomando {medication}\n")
                self.history.append(
                    f"{self.name} se recupero de {self.get_sick()} - {self.get_injuries()} en {self.location.name} y tomando {medication}  en {self.time.get_global_time()}")
            else:
                print(f"{self.name} se recupero de {self.get_injuries()}\n ")
                self.history.append(
                    f"{self.name} se recupero de {self.get_injuries()} en {self.location.name} y en {self.time.get_global_time()}")

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
            print(f"{self.name} se recupero de {self.get_sick()} tomando {medication} \n")
            self.history.append(
                f"{self.name} se recupero de {self.get_sick()} tomando {medication} en {self.location.name} y en {self.time.get_global_time()}")
            self.sick = {k: False if v else v for k, v in self.sick.items()}
            self.injuries = {k: False if v else v for k, v in self.injuries.items()}
            self.injuries['ninguna'] = True
            self.sick['ninguna'] = True

    def move_to(self, new_location: Location):
        if new_location == self.location:
            return
        route = a_estrella(self.map, self.location, new_location)
        route.pop(0)
        path = self.get_places(route)
        for location in path:
            start_time = self.time.get_global_time()
            times = self.estimate_arrival_time(location)
            if isinstance(self, Officer):
                times /= 2
            while True:
                end_time = self.time.get_global_time()  # Registro del tiempo de finalización
                elapsed_time = end_time - start_time  # Cálculo del tiempo transcurrido
                if elapsed_time >= times:  # Condicion seria si ya paso el tiempo
                    previus_location = self.location
                    self.location.people_left(self)
                    self.location = location
                    self.location.people_arrived(self)
                    print(
                        f'{self.name} se movio de {self.location.name} y en el {self.time.get_global_time()} segundo desde {previus_location.name}\n')
                    self.history.append(
                        f'{self.name} se movio de {self.location.name} y en el {self.time.get_global_time()} segundo desde {previus_location.name}\n')
                    break

            if "rob" in self.location.get_state() and not (isinstance(self, Criminal)):
                if isinstance(self, Officer or Detective):
                    print(
                        f'{self.name} detecto un robo')  # si un oficial o un detective llega aun lugar y estan robando
                    self.history.append(
                        f'{self.name}  esta en lugar robado en {self.location.name} y en {self.time.get_global_time()}')
                    people_in_rob = [x for x in location.people_around if 'rob_in_progress' in x.get_state()]
                    if len(people_in_rob) > 0:
                        for i in people_in_rob:
                            chance = self.criminal_chance(i)
                            if chance and not i.state['detenido']:
                                i.state['detenido'] = True
                                i.state['rob_in_progress'] = False
                                print(f'{self.name} atrapo a {i.name} en {self.time.get_global_time()} segundos\n')
                                self.history.append(
                                    f'{self.name} atrapo a {i.name} en {self.time.get_global_time()} segundos')
                                # i.location = self.station
                                # self.station.jail.append(i)
                                i.state['on_jail'] = True
                            elif not chance:
                                print(f'{i.name} escapo')
                    else:

                        self.history.append(
                            f'{self.name} llego tarde a {self.location.name} en {self.time.get_global_time()}')

                    # break

                elif not self.location.state['wait_car']:
                    self.cant_rob_report += 1
                    print('###informando robo por primera vez')
                    self.history.append(
                        f' informando robo por primera vez en {self.location.name} y en {self.time.get_global_time()}')

                    self.location.state['calm'] = False
                    self.location.state['wait_car'] = True
                    station_pol: PoliceDepartment = self.nearest_place(self.locations['pd'][0])
                    if station_pol:
                        self.history.append(
                            f"Calling nearest {station_pol.name} en {self.time.get_global_time()} segundos por {self.name} desde {self.location.name}")
                        station_pol.send_patrol()
                    else:
                        self.history.append('no hay estacion de policia disponible para solucionar robo')
                        self.location.state['rob'] = False

                    if self.location.state['on_fire']:
                        station_fire = self.nearest_place(self.locations['fd'][0])
                        if station_fire:
                            self.history.append(
                                f"Calling nearest {station_fire.name} en {self.time.get_global_time()}  desde {self.location.name} segundos por {self.name}\n")
                            station_fire.send_fire_truck()
                        else:
                            self.history.append('no hay estacion de bomberos disponibles para apagar el fuego')
                            self.location.state['on_fire'] = False
                else:
                    print(f"robo ya informado  en {self.location.name}")
                    self.history.append(f" intento comunicar de robo ya informado  en {self.location.name}")

    def nearest_place(self, place):
        type_of = type(place)
        nearest_place = None
        dist = 999999
        for i in self.all_locations:
            if isinstance(i, type_of) and i.state['enabled']:
                path = a_estrella(self.map, self.location, i)
                path.pop(0)
                route = self.get_places(path)
                place_dist = self.get_total_distance(route)
                if place_dist < dist:
                    nearest_place = i
                    dist = place_dist
        return nearest_place

    def move_to_random_location(self):
        new_location = r.choice(self.location.get_adjacent_locations())
        print(f"{self.name} se va a mover de {self.location.name} a {new_location.name}")
        self.history.append(f'{self.name} dirige a {new_location.name}')
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
        self.history.append(f'{self.name} dirige a {store.name}')
        self.move_to(store)
        store.buy(self)
        self.stay_in_place(5)
        self.go_home()

    def go_to_casino(self):
        casino: Casino = self.nearest_place(self.locations['casinos'][0])
        self.history.append(f'{self.name} dirige a {casino.name}')
        self.move_to(casino)
        casino.play(self)
        self.stay_in_place(5)
        self.go_home()


class Citizen(Agent):
    def __call__(self, time, *args, **kwargs):
        while True:
            if time <= self.time.get_global_time():
                break
            # self.stay_in_place(8)
            if self.get_injuries() != 'ninguna' or self.get_sick() != 'ninguna':
                self.go_to_hospital()
            if self.home.cash > 400:
                print(f'{self.name} va depositar')
                self.go_bank_deposit()
            # if self.home.cash < 100:
            #     print(f'{self.name} esta extrayendo')
            #     self.go_bank_extract()
            # if self.time.get_global_time() >= 22:
            #     print(f'{self.name} esta regresando a su casa')
            aux_mov = r.random()
            if aux_mov < 0.8:
                self.move_to_random_location()
            elif 0.9 > aux_mov >= 0.8:
                self.go_to_casino()
            else:
                self.go_to_store()
            # if self.time.get_global_time() >= 100:
            #     self.go_home()

    def __init__(self, id, name, location, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)


class Officer(Citizen):
    def __init__(self, id, name, location, weapons, vehicle, mastery, time, city, all_locations, house, station):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery
        self.station: PoliceDepartment = station
        self.station.current_officers.append(self)

    def __call__(self, time, *args, **kwargs):
        while True:
            if time <= self.time.get_global_time():
                break
            aux_loc = None
            if 'go_to_rob' in self.get_state():
                for i in self.all_locations:
                    if 'wait_car' in i.get_state():
                        aux_loc = i
                        break
            if aux_loc:
                self.call_of_dutty(aux_loc)
                self.home.collect()

    def call_of_dutty(self, location, criminal=None):
        print(f'{self.name} va a atender crimen en {self.time.get_global_time()} en el lugar {location.name}')
        self.history.append(f'va a atender crimen en {self.time.get_global_time()} en el lugar {location.name}')
        if True:  # quitar
            self.move_to(location)

        location.state['calm'] = True
        location.state['wait_car'] = False
        location.state['rob'] = False
        self.state['go_to_rob'] = False
        print(
            f'{self.name} esta volviendo a la estacion {self.station.name} en el segundo {self.time.get_global_time()}')
        self.return_station()

    def return_station(self):
        self.location = self.station
        self.location.state['enabled'] = True

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


class Fire_Fighter(Citizen):
    def __init__(self, id, name, location, time, city, all_locations, house, station: FireDepartment):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.station = station
        self.station.fire_fighters.append(self)

    def __call__(self, time, *args, **kwargs):

        start_time = self.time.get_global_time()
        while True:
            if time <= self.time.get_global_time():
                break
            aux_loc = None
            if 'go_to_rob' in self.get_state():
                for i in self.all_locations:
                    if 'on_fire' in i.get_state():
                        aux_loc = i
                        break
            if aux_loc:
                self.stop_fire(aux_loc)
                break

    def stop_fire(self, location):
        print(f'moviendose hacia fuego {self.time.get_global_time()}')
        self.history.append(f'moviendose hacia fuego en {location.name} y en {self.time.get_global_time()}')
        self.move_to(location)
        self.stay_in_place(5)
        print('fuego apagado')
        self.history.append(f'se apago fuego en {location.name} y en {self.time.get_global_time()}')
        location.state['on_fire'] = False

        self.move_to(self.station)
        self.state['go_to_rob'] = False
        self.station.state['enabled'] = True


class Detective(Citizen):
    def __init__(self, id, name, location, weapons, mastery, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.weapons = weapons
        self.mastery = mastery

    def investigate(self):
        return NotImplementedError


class Employee(Citizen):
    ##Se podria agregar un parametro de percepcion para que un empleado pueda adelantarse a un robo
    def __call__(self, time, *args, **kwargs):

        while True:
            if time <= self.time.get_global_time():
                break
            aux_random = r.random()
            if aux_random < 0.8:
                self.go_work()
            else:
                aux_random2 = r.randint(0, len(self.sick) - 2)
                self.sick['ninguna'] = False
                self.sick[list(self.sick.keys())[aux_random2]] = True
                self.go_to_hospital()

    def __init__(self, id, name, location, work_place: Location, time, city, all_locations, house):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.hired_in = work_place
        self.hired_in.staff.append(self)
        self.route = self.get_route()
        self.walk_time = self.get_total_distance(self.route)

    def get_route(self):
        route = a_estrella(self.map, self.location, self.hired_in)
        return self.get_places(route)

    def go_work(self):
        self.stay_in_place(20 - self.walk_time)
        self.history.append(f'se dirige a trabajar a {self.hired_in.name} en {self.time.get_global_time()}')
        self.move_to(self.hired_in)
        self.history.append(f'se llego al trabajo  {self.hired_in.name} en {self.time.get_global_time()}')
        self.stay_in_place(50)
        self.history.append(f'se fue del trabajo {self.hired_in.name} en {self.time.get_global_time()}')
        self.home.collect()
        self.go_home()


##no borrar


class Criminal(Agent):

    def __init__(self, id, name, location, weapons, vehicle, time, city, all_locations, house, criminalidad,
                 agresividad, mastery=1):
        super().__init__(id, name, location, time, city, all_locations, house)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery
        self.criminalidad = criminalidad
        self.agresividad = agresividad
        self.gang = []
        self.boss = False
        self.state['on_command'] = False

    def __call__(self, time, *args, **kwargs):
        while True:
            if time <= self.time.get_global_time():
                if self.boss:
                    self.boss.gang.remove(self)
                break
            if 'on_jail' in self.get_state():
                station_pol: PoliceDepartment = self.nearest_place(self.locations['pd'][0])
                self.move_to(station_pol)
                station_pol.jail.append(self)
                self.cant_apresados += 1
                print(f'{self.name} Presooooo!!!!!!!!!!!!!! esperando-------------------------------------------------')
                self.stay_in_place(20)
                self.location.jail.remove(self)
                self.state['on_jail'] = False
                self.state['detenido'] = False
                print(f'{self.name} Liberado.... portate bien tankewe!!')

            if 'on_comand' in self.get_state():
                self.move_to(self.boss.location)
                self.stay_in_place(10)

            self.move_to_random_location()
            if isinstance(self.location, PoliceDepartment):
                continue
            if isinstance(self.location, FireDepartment):
                continue
            if isinstance(self.location, Hospital):
                continue
            if self.gang:
                self.try_robbery_with_band()

    def move_to(self, new_location: Location):
        super().move_to(new_location)
        self.gather_band()

    def gather_band(self):

        criminals = [x for x in self.location.people_around if isinstance(x, Criminal)]
        for c in criminals:
            if (c.mastery <= self.mastery and not c.boss) or (c.boss and c.boss.mastery < self.mastery):
                if c == self: continue
                self.gang.append(c)
                c.boss = self
                print(f"{self.name} recluto {c.name}-----!!!!!!!!!!!!--------!!!!!!!!!!!!-------------!!!!!!!!!!!!!")

    def calculate_rob_time(self, band=False):
        rob_time = 30
        if band:
            rob_time /= 2
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

    def calculate_success_probability(self, band=False):

        ### Faltaria implementar la comunicacion entre los ladrones para que aumente su prob

        powr = len(str(len(self.people_on_sight) - 1))
        success_probability = self.mastery * (
                1 - ((len(self.people_on_sight) - 1) / 10 ** powr))

        if band:
            success_probability += 0.5

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

    def try_robbery_with_band(self):
        full_gang = False
        for i in self.gang:
            i.state['on_command'] = True

        while not full_gang:  # Esperar por los muchachos
            if not self.gang: full_gang = True
            print('Esperando los muchachos')
            for i in self.gang:
                print(i.name)
                print(i.state)
                if 'on_jail' in i.get_state():
                    self.gang.remove(i)
            for i in self.gang:
                if not i in self.location.people_around:
                    break
                full_gang = True

        self.try_robbery(True)

    def try_robbery(self, band=False):
        if self.location == self.home:
            self.move_to_random_location()
            return
        chances = self.calculate_success_probability()
        rob_time = self.calculate_rob_time()  ## Arreglar tiempo de robo
        if band:
            chances += 0.5
            rob_time /= 2
        if chances >= self.criminalidad and 'calm' in self.location.get_state():
            start_time = self.time.get_global_time()
            self.state['rob_in_progress'] = True
            if band:
                for i in self.gang:
                    i.state['rob_in_progress'] = True
            self.location.state['calm'] = False
            self.location.state['rob'] = True
            is_success = r.random() * (1 + self.mastery / 10) + 0.3 if band else r.random() * (1 + self.mastery / 10)
            print(f"Robando {self.location.name} por {self.name}\n")
            if band:
                print(
                    f"Robando {self.location.name} por {self.name} y su banda!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!---------------------------------------------------------\n")

            self.cant_rob += 1
            self.history.append(f"Robando {self.location.name} por {self.name} en {self.time.get_global_time()}")

            hurt_someone = r.random()
            while True:
                end_time = self.time.get_global_time()
                elapse_time = end_time - start_time
                if elapse_time >= rob_time:
                    if hurt_someone >= self.agresividad:  ## Modificar esta probabilidad luego
                        if len(self.people_on_sight) > 0:
                            person = r.choice(self.people_on_sight)
                            print(
                                f'Se le va a meter la tiza a {person.name} --------------------------------------------')
                            if person != self:
                                injure = r.choice(list(self.injuries.keys()))
                                self.cant_heridos += 1
                                if injure == 'quemadura':
                                    self.cant_incendios += 1
                                    self.location.state['on_fire'] = True
                                self.history.append(
                                    f'hirio a {person.name} en {self.time.get_global_time()} de {injure}')
                                person.injuries[injure] = True
                                person.injuries['ninguna'] = False
                            # print(person.get_injuries())
                    break
            if 'detenido' in self.get_state():
                self.state['rob_in_progress'] = False
                print(f'{self.name} ha sido apresado\n')
                self.history.append(f'{self.name} ha sido apresado en {self.time.get_global_time()}')
                return

            if is_success < chances:
                self.state['rob_in_progress'] = False
                if band:
                    for i in self.gang:
                        i.state['rob_in_progress'] = False
                        i.state['on_command'] = False
                stolen_cash = self.location.cash * (self.mastery / 10)
                self.home.cash += stolen_cash / 2 if band else stolen_cash
                if band:
                    print('Se repartio el dinero del robo entre la banda')
                    for i in self.gang:
                        i.home.cash += stolen_cash / (len(self.gang) / 2)
                self.cant_dinero_rob += stolen_cash
                self.location.cash -= stolen_cash
                print(f'Dinero robado {stolen_cash} por {self.name}')
                self.history.append(
                    f'Dinero robado {stolen_cash} por {self.name} en {self.location.name} y en {self.time.get_global_time()}')
                self.mastery += 1
            else:
                self.state['rob_in_progress'] = False
                if band:
                    for i in self.gang:
                        i.state['rob_in_progress'] = False
                        i.state['on_command'] = False
                print(f'robo fallido en {self.location.name} en {self.time.get_global_time()} segundos\n')
                self.history.append(f'robo fallido en {self.location.name} en {self.time.get_global_time()} segundos')
                self.mastery += 0.2
        else:
            self.state['rob_in_progress'] = False
            if band:
                for i in self.gang:
                    i.state['rob_in_progress'] = False
                    i.state['on_command'] = False

            print(f'posbilidad de robo muy baja en {self.location.name}\n')
            self.move_to(self.all_locations[r.randint(0, 10)])

        # self.move_to(self.all_locations[r.randint(0, 10)])
