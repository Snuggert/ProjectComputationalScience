import random


# Using data from Thesis of Matthew C. Snare Msc. Civil engineering.
# Modelling using his data of a 1998 Honda Accord
# The Rakha et al. constant power model.
def car_acc(v_speed):
    # constants
    v_mass = 1770.  # Kilos
    friction_coeff = 0.6  # Coefficient Mu
    engine_eff = 0.75  # Coefficient Eta
    engine_power = 111.9  # in kW

    F_t = 3600 * engine_eff * (engine_power / v_speed)
    F_max = 9.8066 * v_mass * friction_coeff
    F = min(F_t, F_max)  # Tractive Force

    constant_aero = 0.047285
    C_d = 0.34  # Air drag coefficient
    C_h = 0.95  # Altitude coefficient
    A = 2.12  # Frontal area in m^2
    R_a = constant_aero * C_d * C_h * A * v_speed * v_speed

    C_r = 1.25  # Rolling resistance coefficient
    c_2 = 0.0328  # Rolling resistance coefficient
    c_3 = 4.575  # Rolling resistance coefficient

    # Rolling resistance
    R_r = 9.8066 * C_r * (c_2 * v_speed + c_3) * (v_mass / 1000.)

    # Grade resistance is zero because we assume constant height of the road.
    R_g = 0

    R = R_a + R_r + R_g

    return (F - R) / v_mass


def truck_acc(speed):
    return 2.


def broken_acc(speed):
    return 0


class Vehicle:
    v_properties = {"car": (car_acc, 10., 3, 1),
                    "truck": (truck_acc, 4., 2, 4),
                    "broken": (broken_acc, 10., 3, 1)}

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
    return int(random.normalvariate(0., 7.) * 10) / 10.0
