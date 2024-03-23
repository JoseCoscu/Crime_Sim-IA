class Location:
    def __init__(self, name: str):
        self.name = name
        self.connected_to = {}
        self.people_around = []

    def add_row(self, place, dist):
        self.connected_to[place.name] = dist
        place.connected_to[self.name] = dist

    def people_arrived(self, people):
        self.people_around.append(people)

    def people_left(self, people):
        self.people_around.remove(people)


class PoliceDepartment(Location):
    def __init__(self, name, officers, detectives, cars):
        super().__init__(name)
        self.current_officers = officers
        self.current_detectives = detectives
        self.current_cars = cars

    def send_patrol(self, cars, place):
        return NotImplementedError


class FireDepartment(Location):
    def __init__(self, name, fire_fighters, trucks, water):
        super().__init__(name)
        self.fire_fighters = fire_fighters
        self.trucks = trucks
        self.water = water

    def send_fire_truck(self, fire_fighters, truck, water, location):
        return NotImplementedError


class Hospital(Location):
    def __init__(self, name, ambulances, rooms, doctors):
        super().__init__(name)
        self.ambulances = ambulances
        self.rooms = rooms
        self.doctors = doctors

    def send_ambulance(self, place):
        return NotImplementedError


class Store(Location):

    def __init__(self, name, stock, staff, cash, product_worth):
        super().__init__(name)
        self.staff = staff
        self.cash = cash
        self.product_w = product_worth
        self.stock = stock

    # self.is_open = False Poner esto en los estados del nodo ???????

    def restock(self):
        self.stock = 100

    def call_police(self):
        return NotImplementedError

    def call_fire_f(self):
        return NotImplementedError


class GasStation(Location):

    def __init__(self, name, gas, staff, cash):
        super().__init__(name)
        self.gas = gas
        self.staff = staff
        self.cash = cash

    def restock_gas(self):
        self.gas = 100


hos = Hospital("Ramon", 5, 20, 8)
ps = PoliceDepartment("PNR", 10, 5, 3)

hos.add_row(ps, 10)

print(ps.current_cars)
print(hos.connected_to)
