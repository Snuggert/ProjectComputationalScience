from car import Car


class World:
    worldsize = 0
    cars = []

    def __init__(self, worldsize):
        self.id = id
        self.worldsize = worldsize

    def add_car(self, speed, location):
        self.cars.append(Car(speed, location))
