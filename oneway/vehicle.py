import random


class Vehicle:
    v_properties = {"car": (5., 10., 3, 1), "truck": (3., 4., 2, 4),
                    "broken": (0., 10., 3, 1)}

    def __init__(self, speed, location, v_type, tick):
        self.t_react = reactiontime(tick)
        self.auto_max = automax()
        buffer_size = int(round(self.t_react / tick, 0)) + 1
        self.acc = [0] * buffer_size
        self.speed = speed
        self.location = location
        self.max_acc, self.max_brake, self.length, self.mass = \
            self.v_properties[v_type]
        self.loc_speed_old = (location - speed * tick, speed)
        self.change_lane = []

    def set_next_acc(self, new_acc):
        new_acc = min([new_acc, self.max_acc])
        new_acc = max([new_acc, -self.max_brake])

        self.acc.remove(self.acc[0])
        self.acc.append(new_acc)

    def accelerate(self, edge_max_speed, acceleration, timedelta):
        max_speed = edge_max_speed(self.location)

        # driver faster than allowed
        if self.speed > max_speed + self.auto_max:
            acceleration = -2
            self.set_next_acc(acceleration)
            if self.acc[0] < 0:
                self.speed += self.acc[0] * timedelta
                
        # accelerate as much as possible
        else:
            self.set_next_acc(acceleration)
            self.speed += self.acc[0] * timedelta

            # maximum speed reached
            self.speed = min([self.speed, max_speed + self.auto_max])

        self.speed = max([self.speed, 0])

        self.loc_speed_old = self.loc_speed_old[0], self.speed


def reactiontime(tick):
    mu, sigma, theta = (0.18, 0.01, 0.02)
    gau = random.gauss(mu, sigma)
    exp = random.gammavariate(1, theta)
    if(gau <= 0):
        return reactiontime()
    return int((gau + exp) * (1 / tick) + 0.5) / (1 / tick)


def automax():
    return int(random.normalvariate(0., 2.) * 10) / 10.0
