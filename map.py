from locations_class import *

police_departments = []
hospitals = []
fire_departments = []
houses = []
stores = []
gs_stations = []
banks = []
casinos = []

for i in range(1, 21):
    houses.append(Hause(i, "House_" + str(i)))

for i in range(1, 5):
    stores.append(Store(i, "Store_" + str(i), 0, [], 0, 0))
    gs_stations.append(GasStation(i, "Gas_Station_" + str(i), 0, [], 0))

for i in range(1, 3):
    hospitals.append(Hospital(i, "Hospital_" + str(i), [], 0, []))
    banks.append(Bank(i, "Bank_" + str(i)))
    casinos.append(Casino(i, "Bank_" + str(i)))
    police_departments.append(PoliceDepartment(i, "PNR_" + str(i), [], [], []))

## Police Departments Connections----------------

police_departments[0].add_row(houses[0:3], 1, 5)
police_departments[0].add_row([stores[0], gs_stations[0]], 1, 5)
police_departments[1].add_row([stores[3], banks[1], houses[19], casinos[1]], 3, 10)

## Hospitals Connections ---------------------------

hospitals[0].add_row([gs_stations[3], houses[15], houses[18], casinos[1]], 5, 8)
hospitals[1].add_row([houses[13], houses[14], houses[16], gs_stations[2], stores[2]], 4, 9)

## Banks Connections -----------------------------------

banks[0].add_row([houses[8], houses[11],houses[12],houses[14]])
