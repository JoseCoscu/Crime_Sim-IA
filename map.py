import random

from locations_class import *
from agent_class import *
import random as r
from graph import *
import threading
from timer import TimeMeter, time_updater
#from text_process import habitantes, oficiales, criminales, bomberos, indice_agresividad, indice_crim




police_departments = []
hospitals = []
fire_departments = []
houses = []
stores = []
gs_stations = []
banks = []
casinos = []
all_locations = []
time_meter = TimeMeter()

# region Creacion de locaclizaciones
## Creating Locations--------------------

for i in range(1, 21):
    houses.append(House(i, "House_" + str(i)))
    all_locations.append(houses[-1])

for i in range(1, 5):
    stores.append(Store(i, "Store_" + str(i), 0, [], 300, 1000))
    gs_stations.append(GasStation(i, "Gas Station_" + str(i), 0, [], 300))

    all_locations.append(stores[-1])
    all_locations.append(gs_stations[-1])

for i in range(1, 3):
    hospitals.append(Hospital(i, "Hospital_" + str(i), [], 0, []))
    banks.append(Bank(i, "Bank_" + str(i), []))
    casinos.append(Casino(i, "Casino_" + str(i), []))
    police_departments.append(PoliceDepartment(i, "PNR_" + str(i), [], [], []))
    fire_departments.append(FireDepartment(i, "Fire Department_" + str(i), [], [], 100))

    all_locations.append(hospitals[-1])
    all_locations.append(banks[-1])
    all_locations.append(casinos[-1])
    all_locations.append(police_departments[-1])
    all_locations.append(fire_departments[-1])

## Police Departments Connections----------------

police_departments[0].add_row(houses[0:3], 1, 5)
police_departments[0].add_row([stores[0], gs_stations[0]], 1, 5)
police_departments[1].add_row([stores[3], banks[1], houses[19], casinos[1]], 3, 10)

## Hospitals Connections ---------------------------

hospitals[0].add_row([gs_stations[3], houses[15], houses[18], casinos[1]], 5, 8)
hospitals[1].add_row([houses[13], houses[14], houses[16], gs_stations[2], stores[2]], 4, 9)

## Banks Connections -----------------------------------

banks[0].add_row([houses[8], houses[11], houses[12], houses[14], stores[2]], 5, 10)
banks[1].add_row([houses[16], houses[17], stores[3], fire_departments[1]], 5, 6)

## Casinos Connecctions --------------------------------------------

casinos[0].add_row([houses[15], houses[8], houses[9], houses[12], houses[14], houses[16], gs_stations[2],
                    banks[1]], 7, 10)
casinos[1].add_row(houses[17:20], 3, 5)

## Fire Departments Connections ----------------------------------


fire_departments[0].add_row([houses[10], houses[18], houses[0], stores[1], gs_stations[1]], 3, 6)
fire_departments[1].add_row([houses[16], gs_stations[2]], 3, 8)

## Stores Connections ---------------------------------------------

stores[0].add_row([houses[0], houses[1], houses[6]], 5, 10)
stores[1].add_row([houses[0], houses[8], houses[3], houses[10]], 5, 15)
stores[2].add_row([houses[7], houses[5], houses[4], houses[13], gs_stations[0]], 10, 20)
stores[3].add_row([houses[19], houses[17], houses[9], houses[16], gs_stations[3]], 8, 15)

## Gas Stations Connections ---------------------------------------

gs_stations[0].add_row(houses[1:8], 3, 8)
gs_stations[0].add_row([houses[8]], 5, 9)
gs_stations[1].add_row([houses[15], houses[18], houses[9], houses[8]], 2, 10)
gs_stations[2].add_row([houses[12], houses[14], houses[16]], 2, 7)
gs_stations[3].add_row([houses[16], houses[19], houses[15], houses[18]], 3, 10)

## Houses Connections -----------------------------------------------

houses[11].add_row([fire_departments[1], houses[7], stores[2]], 6, 8)
houses[2].add_row([houses[4]], 3, 4)
# endregion


## Creating Agents --------------------------------------------------

all_agents = []
criminals = []
citizens = []
officers = []
employee = []
fire_fighters = []
id = 1
habitantes=30
criminales=8
bomberos=3
oficiales=7
indice_agresividad='Alto'
indice_crim='Alto'

ciudadanos = habitantes - criminales - bomberos - oficiales
empleados = int(ciudadanos / 2)
ciudadanos = int(ciudadanos / 2)

if indice_agresividad == 'Alto':
    indice_agresividad = 0.2
if indice_agresividad == 'Medio':
    indice_agresividad = 0.5
if indice_agresividad == 'Bajo':
    indice_agresividad = 0.8

if indice_crim == 'Alto':
    indice_crim = 0.2
if indice_crim == 'Medio':
    indice_crim = 0.5
if indice_crim == 'Bajo':
    indice_crim = 0.8

G = create_map(all_locations)

for i in range(0, empleados):
    house = r.choice(houses)
    store = r.choice(stores)
    all_agents.append(
        Employee(id, 'Employee_' + str(i), r.choice(houses), store, time_meter, G, all_locations, house))
    employee.append(all_agents[-1])

for i in range(0, ciudadanos):
    house = r.choice(houses)
    all_agents.append(Citizen(id, 'Citizen_' + str(i), house, time_meter, G, all_locations, house))
    citizens.append(all_agents[-1])

for i in range(0, criminales):
    all_agents.append(
        Criminal(id, 'Criminal_' + str(i), r.choice(all_locations), [], [], time_meter, G, all_locations,
                 r.choice(houses), indice_crim, indice_agresividad, 1))
    criminals.append(all_agents[-1])

for i in range(0, oficiales):
    station = r.choice(police_departments)
    all_agents.append(
        Officer(id, 'Officer_' + str(i), station, [], [], 10, time_meter, G, all_locations,
                r.choice(houses),
                station))
    officers.append(all_agents[-1])
    officers[-1].state['work'] = True

for i in range(0, bomberos):
    fire_d = r.choice(fire_departments)
    all_agents.append(
        Fire_Fighter(id, 'Fire_Fighter_' + str(i), fire_d, time_meter, G, all_locations, r.choice(houses),
                     fire_d))
    fire_fighters.append(all_agents[-1])


def citizens_threads(i):
    citizens[i](100)


def criminal_threads(i):
    criminals[i](100)


def employee_threads(i):
    employee[i](100)


def officers_threads(i):
    officers[i](100)


def fire_fighters_threads(i):
    fire_fighters[i](100)


#
t = []
# # for i in range(0, 1):
# #     t.append(threading.Thread(target=citizens_threads, args=(i,)))
# #     t[-1].start()
#
## hilo bomberos
for i in range(0, len(fire_fighters)):
    t.append(threading.Thread(target=fire_fighters_threads, args=(i,)))

# # hilos de oficiales
for i in range(0, len(officers)):
    t.append(threading.Thread(target=officers_threads, args=(i,)))

# ## hilos de criminales
for i in range(0, len(criminals)):
    t.append(threading.Thread(target=criminal_threads, args=(i,)))

## hilos de empleados
for i in range(0, len(employee)):
    t.append(threading.Thread(target=employee_threads, args=(i,)))

### hilos de citizens
for i in range(0, len(citizens)):
    t.append(threading.Thread(target=citizens_threads, args=(i,)))

time_updater_thread = threading.Thread(target=time_updater, args=(time_meter,))
time_updater_thread.daemon = True  # El hilo se detendrá cuando el programa principal termine
time_updater_thread.start()
th = [False for x in t]
d = {}
for i in t:
    d[i] = False

i = 0
while i < len(t):
    threads = [x for x in list(d.keys()) if not d[x]]
    m = random.choice(threads)
    m.start()
    d[m] = True
    i += 1

# for i in t:
#     i.start()
for i in list(d.keys()):
    i.join()

print(
    f"Informacion sobre {criminals[0].name} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for i in criminals[0].history:
    print(i)

cant_robs = 0
cant_heridos = 0
cant_rob_atendidos = 0
cant_apresados = 0
cant_dinero_rob = 0
cant_rob_report = 0
cant_incendios = 0
cant_incendios_att = 0

for i in all_agents:
    cant_robs += i.cant_rob
    cant_heridos += i.cant_heridos
    cant_apresados += i.cant_apresados
    cant_dinero_rob += i.cant_dinero_rob
    cant_incendios += i.cant_incendios
    cant_rob_report += i.cant_rob_report
print(f'Cant Robos:{cant_robs}\nCant heridos: {cant_heridos}\nCant Incendios:{cant_incendios}\n'
      f'Cant Dinero Robado: {cant_dinero_rob}\nCant Criminales Capturados: {cant_apresados}\n'
      f'Cant Rob Report: {cant_rob_report}')
# print(all_agents[0].history)
# for i in officers[0].history:
#     print(i)
# citizens[0]()

# show_locations(G)

# print(all_agents[0].get_distance(route[1]))
