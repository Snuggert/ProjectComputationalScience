import math
import matplotlib.pyplot as plt
from vehicle import Vehicle


class Edge:
    vehicles = []
    max_speed = 40
    marge = 1.0

    def __init__(self, locations):
        self.id = id
        self.locations = locations
        self.edgesize = \
            math.sqrt(math.pow(locations[1][0] - locations[0][0], 2) +
                      math.pow(locations[1][1] - locations[0][1], 2))

    def add_vehicle(self, speed, location, v_type):
        self.vehicles.append(Vehicle(speed, location, v_type))

    def move_vehicles(self, timedelta):
        if(len(self.vehicles) == 0):
            return

        while True:
            if(self.vehicles[0].location > self.edgesize):
                self.vehicles.pop(0)
            else:
                break
            if(len(self.vehicles) == 0):
                return

        for i, vehicle in enumerate(self.vehicles):
            '''
            Move vehicle
            '''
            print "auto %d begint op locatie %.2f met snelheid %.2f" % \
                (i, vehicle.location, vehicle.speed[0])
            new_location = vehicle.location + timedelta * 0.5 * \
                (vehicle.speed[0] + vehicle.speed[1])
            current_speed = vehicle.speed[1]
            print "rijdt naar %.2f met eindsnelheid %.2f" % \
                (new_location, current_speed)
            vehicle.location = new_location

            # make a decision for each vehicle (that is not in front)
            if(i is not 0):
                '''
                Find the gap and other constants
                '''
                vehicle_infront = self.vehicles[i - 1]
                vel0 = vehicle_infront.speed[0]
                min_dist = vehicle_infront.length + self.marge
                gap = vehicle_infront.location - vehicle.location
                params = min_dist, vehicle.max_brake, vehicle.t_react
                needed_gap = find_min_gap(vel0, params)
                print "--> Gat is %.2f" % gap

                '''
                Check for collision
                '''
                print "Needed_gap is %.2f" % needed_gap
                if gap < vehicle_infront.length:
                    print "FATAL ERROR!!! >:( "
                    self.vehicles = []

                relative_speed = current_speed - vehicle_infront.speed[0]
                min_gap = find_min_gap(current_speed, params)
                print "min_gap: %.2f" % min_gap

                '''
                Driving too close to the vehicle in front
                '''
                if gap < min_gap:
                    new_speed = 2. / timedelta * (gap - min_gap) + 2. * vel0 - current_speed
                    acc_adj = new_speed - current_speed
                    if acc_adj < - vehicle.max_brake:
                        acc_adj = - vehicle.max_brake
                    print "te dichtbij: verander snelheid met : %.2f" % acc_adj
                    vehicle.set_next_speed(current_speed + acc_adj)
                    continue

                '''
                Driving the same speed as the vehicle in front
                '''
                if abs(relative_speed) < 0.5:
                    if gap > min_gap + vehicle.max_accelerate * timedelta * timedelta:
                        vehicle.accelerate(self.max_speed, vehicle.max_accelerate, timedelta)
                        print "accelereren"

                    else:
                        print "zelfde snelheid houden"
                        vehicle.set_next_speed(vel0)
                    continue

                '''
                Driving slower than the vehicle in front
                '''
                if relative_speed < 0:
                    if gap < needed_gap:
                        delta_t = 2. * (needed_gap - gap) / (-relative_speed)
                        acc_adj = (-relative_speed) / delta_t
                        if acc_adj > vehicle.max_accelerate:
                            acc_adj = vehicle.max_accelerate
                        print "hij versnelt met %.2f m/s2 (t = %.2f)" % \
                            (acc_adj, delta_t)
                    else:
                        acc_adj = vehicle.max_accelerate
                        print "maximaal accelereren"

                    vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                    continue



                '''
                Driving faster than the vehicle in front
                '''
                delta_t = 2. * (gap - needed_gap) / relative_speed
                acc_adj = relative_speed / delta_t
                if (acc_adj > 2.0 or gap < 2 * needed_gap):
                    new_speed = current_speed - acc_adj
                    acc_adj = current_speed - new_speed
                    if acc_adj > vehicle.max_brake:
                        acc_adj = vehicle.max_brake
                        print "remmen!"
                    print "hij gaat zijn snelheid aanpassen met %.2f m/s2" % \
                        (-acc_adj)
                    vehicle.set_next_speed(new_speed)
                else:
                    print "hij gaat versnellen (t = %.2f, a was %.2f m/s2)" % \
                        (delta_t, -acc_adj)
                    vehicle.accelerate(self.max_speed, vehicle.max_accelerate, timedelta)

            else:
                vehicle.accelerate(self.max_speed, vehicle.max_accelerate,timedelta)
            print ""

    def plot_vehicles(self):
        vehicles_xy = [[], []]
        for vehicle in self.vehicles:
            vehicles_xy[0].append(vehicle.location)
            vehicles_xy[1].append(1)
        plt.plot(vehicles_xy[0], vehicles_xy[1], 'bs')
        plt.axis([0, self.edgesize, 0, 2])
        plt.draw()
        plt.pause(0.1)
        plt.clf()

def find_min_gap(v_current, params):
    min_dist, max_brake, t_react = params
    t_brake_abs = v_current / max_brake
    x_brake_abs = (v_current * t_brake_abs) / 2.
    gap = x_brake_abs + min_dist
    return gap