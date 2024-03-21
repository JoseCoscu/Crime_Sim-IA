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


class Hospital(Location):
    def __init__(self, name, ambulances, rooms, doctors):
        super().__init__(name)
        self.ambulances = ambulances
        self.rooms = rooms
        self.doctors = doctors

    def send_ambulance(self, place):
        return NotImplementedError





hos = Hospital("Ramon", 5, 20, 8)
ps = PoliceDepartment("PNR", 10, 5, 3)

hos.add_row(ps, 10)

print(ps.current_cars)
print(hos.connected_to)
