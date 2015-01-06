class Car:
    max_brake = -10
    max_accellerate = 2
    t_react = 1

    def __init__(self, speed, location):
        self.speed = [speed, speed, ]
        self.location = location
        self.next_speed = speed
        

    def set_location(self, location):
        self.location = location

    def set_next_speed(self, new_speed):
        self.speed.remove(self.speed[0])
        self.speed.append(new_speed)

    def accellerate(self, max_speed, timedelta):
        new_speed = self.speed + self.max_accellerate * timedelta
        if new_speed > max_speed:
            new_speed = max_speed
                    
        self.set_next_speed(new_speed)
