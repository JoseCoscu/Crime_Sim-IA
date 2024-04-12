from locations_class import *
from agent_class import *
import random as r
from graph import *
from timer import Time

police_departments = []
hospitals = []
fire_departments = []
houses = []
stores = []
gs_stations = []
banks = []
casinos = []
all_locations = []

timer = Time(0, 0, 0)

## Creating Locations--------------------

for i in range(1, 21):
    houses.append(House(i, "House_" + str(i)))
    all_locations.append(houses[-1])

for i in range(1, 5):
    stores.append(Store(i, "Store_" + str(i), 0, [], 100, 1000))
    gs_stations.append(GasStation(i, "Gas Station_" + str(i), 0, [], 100))

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

## Creating Agents --------------------------------------------------

all_agents = []
criminals = []
citizens = []
id = 1

G = create_map(all_locations)

all_agents.append(Criminal(id, 'Criminal_' + str(id), houses[0], [], [], timer, G, all_locations, houses[1]))
criminals.append(all_agents[-1])
id += 1
all_agents.append(Citizen(id, 'Citizen_' + str(id), houses[0], timer, G, all_locations, houses[0]))
citizens.append(all_agents[-1])

# while (True):
#     for i in all_agents:
#         if isinstance(i, Citizen):
#             i()
#         if isinstance(i,Criminal):
#             i()
#
#     time += 1
#     if time >= 10:
#         break


criminals[0].try_robbery()
citizens[0]()

# show_locations(G)

# print(all_agents[0].get_distance(route[1]))
