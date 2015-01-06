class Car:
    speed = 0
    location = 0

    next_speed = 0

    max_brake = -5
    max_accellerate = 2

    def __init__(self, speed, location):
        self.speed = speed
        self.location = location

    def set_location(self, location):
        self.location = location

    def set_next_speed(self, new_speed):
        self.next_speed = new_speed

    def apply_next_speed(self):
        self.speed = self.next_speed
