from locations_class import Location


class Agent:

    def __init__(self, id, name, location: Location):
        self.id = id
        self.name = name
        self.location = location
        self.location.people_arrived(self)

    # Para esta funcion ffaltaria calcular el tiempo que demora dicho movimiento de un lugar a otro basandose en lo
    # implementado en la clase de grafos
    def move_to(self, new_location: Location):
        self.location.people_left(self)
        self.location = new_location
        self.location.people_arrived(self)


class Officer(Agent):
    def __init__(self, id, name, location, weapons, vehicle, mastery):
        super().__init__(id, name, location)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def call_of_dutty(self):
        return NotImplementedError


class Detective(Agent):
    def __init__(self, id, name, location, weapons, vehicle, mastery):
        super().__init__(id, name, location)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def investigate(self):
        return NotImplementedError


class Criminal(Agent):
    def __init__(self, id, name, location, weapons, vehicle, mastery):
        super().__init__(id, name, location)
        self.weapons = weapons
        self.vehicle = vehicle
        self.mastery = mastery

    def try_robbery(self):
        return NotImplementedError


class Employee(Agent):
    ## Se podria agregar un parametro de percepcion para que un empleado pueda adelantarse a un robo

    def __init__(self, id, name, location, work_place: Location):
        super().__init__(id, name, location)
        self.hired_in = work_place

    def go_work(self):
        self.move_to(self.hired_in)
