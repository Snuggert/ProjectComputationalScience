class Vehicle:
    t_react = 1.
    v_properties = [(2., 10.,3), (3., 12., 2), (0., 10., 3)]

    def __init__(self, speed, location, v_type):
        self.speed = [speed, speed, ]
        self.location = location
        self.v_type = v_type
        self.max_accelerate, self.max_brake, self.length = self.v_properties[v_type]

    def set_location(self, location):
        self.location = location

    def set_next_speed(self, new_speed):
        self.speed.remove(self.speed[0])
        if new_speed < 0:
            new_speed = 0.
        self.speed.append(new_speed)

    def accelerate(self, max_speed, timedelta):
        new_speed = self.speed[1] + self.max_accelerate * timedelta
        if new_speed > max_speed:
            new_speed = max_speed

        self.set_next_speed(new_speed)
