import random


class Vehicle:
    v_properties = {"car":(2., 10., 3, 1), "truck": (3., 12., 2, 1), \
    "broken": (0., 10., 3, 1)}

    def __init__(self, speed, location, v_type, tick):
        self.t_react = reactiontime(tick)
        buffer_size = int(self.t_react / tick) + 1
        self.speed = [speed] * buffer_size
        self.location = location
        self.max_acc, self.max_brake, self.length, self.mass = \
            self.v_properties[v_type]

    def set_next_speed(self, new_speed):
        if new_speed < 0:
            new_speed = 0.

        self.speed.remove(self.speed[0])
        self.speed.append(new_speed)

    def accelerate(self, max_speed, acceleration, timedelta):
        if self.speed[1] > max_speed:
            self.set_next_speed(self.speed[1] - 2)
            return

        if acceleration > self.max_acc:
            acceleration = self.max_acc

        new_speed = self.speed[1] + acceleration * timedelta
        if new_speed > max_speed:
            new_speed = max_speed

        self.set_next_speed(new_speed)


def reactiontime(tick):
    mu, sigma, theta = (0.19, 0.01, 0.02)
    gau = random.gauss(mu, sigma)
    exp = random.gammavariate(1, theta)
    if(gau <= 0):
        return reactiontime()
    return int((gau + exp) * (1 / tick) + 0.5) / (1 / tick)
