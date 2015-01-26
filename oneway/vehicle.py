import random

# Using data from Thesis of Matthew C. Snare Msc. Civil engineering.
# Modelling using his data of a 1998 Honda Accord
# The Rakha et Lucic. variable power model with constant power.
def car_acc(v_speed, weight):
    v_speed_km = v_speed * 3.6  # m/s to km/h
    # constants
    v_mass = weight  # Kilos
    axle_mass = 0.610  # Mass on tractive Axle
    friction_coeff = 0.6  # Coefficient Mu
    engine_eff = 0.75  # Coefficient Eta
    engine_power = 111.9  # in kW

    F_max = 9.8066 * v_mass * axle_mass * friction_coeff
    try:
        F_t = 3600 * engine_eff * (engine_power / v_speed_km)
    except ZeroDivisionError:
        F_t = F_max
    F = min(F_t, F_max)  # Tractive Force

    constant_aero = 0.047285
    C_d = 0.34  # Air drag coefficient
    C_h = 0.95  # Altitude coefficient
    A = 2.12  # Frontal area in m^2
    R_a = constant_aero * C_d * C_h * A * v_speed_km * v_speed_km

    C_r = 1.25  # Rolling resistance coefficient
    c_2 = 0.0328  # Rolling resistance coefficient
    c_3 = 4.575  # Rolling resistance coefficient

    # Rolling resistance
    R_r = 9.8066 * C_r * (c_2 * v_speed_km + c_3) * (v_mass / 1000.)

    # Grade resistance is zero because we assume constant height of the road.
    R_g = 0

    R = R_a + R_r + R_g

    a = (F - R) / v_mass  # m/s^2
    return a


# Using data from Rakha and Lucic variable power paper.
# The Rakha et Lucic. variable power model with constant power.
def truck_acc(v_speed, weight):
    v_speed_km = v_speed * 3.6
    # constants
    v_mass = weight  # Kilos
    axle_mass = 0.410  # Mass on tractive Axle
    friction_coeff = 0.6  # Coefficient Mu
    engine_eff = 0.75  # Coefficient Eta
    engine_power = 320.  # in kW

    F_max = 9.8066 * v_mass * axle_mass * friction_coeff
    try:
        F_t = 3600 * engine_eff * (engine_power / v_speed_km)
    except ZeroDivisionError:
        F_t = F_max
    F = min(F_t, F_max)  # Tractive Force

    constant_aero = 0.047285
    C_d = 0.34  # Air drag coefficient
    C_h = 0.95  # Altitude coefficient
    A = 3.5  # Frontal area in m^2
    R_a = constant_aero * C_d * C_h * A * v_speed_km * v_speed_km

    C_r = 1.25  # Rolling resistance coefficient, for radial tires.
    c_2 = 0.0328  # Rolling resistance coefficient
    c_3 = 4.575  # Rolling resistance coefficient

    # Rolling resistance
    R_r = 9.8066 * C_r * (c_2 * v_speed_km + c_3) * (v_mass / 1000.)

    # Grade resistance is zero because we assume constant height of the road.
    R_g = 0

    R = R_a + R_r + R_g

    a = (F - R) / v_mass  # m/s^2
    return a


# Using data from Rakha et Lucic paper of truck weight distribution.
def truck_weight():
    percentage = random.random() * 100.
    intervals = [5, 10, 26, 40, 60, 74, 98]
    weights = [6804, 11340, 15876, 20412, 24947, 29483, 34019, 38555]

    for index, upper in enumerate(intervals):
        if percentage < upper:
            return weights[index]

    return weights[-1]

def broken_acc(speed):
    return 0


class Vehicle:
    v_properties = {"car": (car_acc, 10., 3, 1770.),
                    "truck": (truck_acc, 4., 2, truck_weight()),
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
        self.wants_to_go_right = False
        self.extra_acc_adj = 0.
        self.use_extra = False

    def set_next_acc(self, new_acc):
        if self.use_extra and new_acc >= 0. and self.speed > 0:
            new_acc = self.extra_acc_adj

        new_acc = min([new_acc, self.max_acc(self.speed)])
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
        return reactiontime(tick)
    return int((gau + exp) * (1 / tick) + 0.5) / (1 / tick)


def automax():
    mu, sigma, theta = 0, 0.4, 1.
    gau = random.gauss(mu, sigma)
    exp = random.gammavariate(1, theta)
    return gau + exp
