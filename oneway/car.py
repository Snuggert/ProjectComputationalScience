class Car:
    speed = 0
    location = 0

    max_brake = -5
    max_accellerate = 2
    max_speed = 15

    def __init__(self, speed, location):
        self.speed = speed
        self.location = location

    def set_location(self, location):
        self.location = location
