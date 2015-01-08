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

    def find_min_gap(self, v_current, v_infront, min_dist, max_brake, t_react):
        t_brake_abs = v_current[1] / max_brake
        x_brake_abs = (v_current[1] * t_brake_abs) / 2.
        x_reaction = (v_current[0] + v_current[1]) / 2. * t_react
        gap = x_brake_abs + x_reaction + min_dist
        return gap


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
            print "auto %d begint op locatie %.1f met snelheid %.1f" % \
                (i, vehicle.location, vehicle.speed[0])
            new_location = vehicle.location + timedelta * 0.5 * \
                (vehicle.speed[0] + vehicle.speed[1])
            print "rijdt naar %.1f met eindsnelheid %.1f" % \
                (new_location, vehicle.speed[1])
            vehicle.location = new_location

            # make a decision for each vehicle (that is not in front)
            if(i is not 0):
                # find gap
                vehicle_infront = self.vehicles[i - 1]
                min_dist = vehicle_infront.length + self.marge
                gap = vehicle_infront.location - vehicle.location
                print "--> Gat is %.2f" % gap
                if gap < vehicle_infront.length:
                    print "FATAL ERROR!!! >:( "

                relative_speed = vehicle.speed[1] - vehicle_infront.speed[0]
                min_gap = self.find_min_gap(vehicle.speed, vehicle_infront.speed, min_dist,\
                    vehicle.max_brake, vehicle.t_react)

                '''
                Driving slower than the vehicle infront
                '''
                if relative_speed < 0:
                    vehicle.accelerate(self.max_speed, timedelta)
                    print "hij gaat versnellen"
                    continue

                print "Snelheid auto voor zich is %.1f" % vehicle_infront.speed[0]
                print "Relatieve snelheid: %.1f" % relative_speed

                print "min_gap: %.2f" % min_gap

                '''
                Driving the same speed as the vehicle infront
                '''
                if abs(relative_speed) < 0.01:
                    if gap < min_gap:
                        new_speed = vehicle.speed[1] - vehicle.max_accelerate * timedelta
                        vehicle.set_next_speed(new_speed)
                        print "iets vertragen" 

                    elif gap > min_gap + vehicle.max_accelerate * timedelta * timedelta:
                        vehicle.accelerate(self.max_speed, timedelta)
                        print "accelereren"

                    else:
                        print "zelfde snelheid houden"
                        vehicle.set_next_speed(vehicle.speed[1])
                    continue

                '''
                Driving faster than the vehicle infront
                '''
                vel = vehicle_infront.speed[0]
                needed_gap = self.find_min_gap([vel, vel],[vel, vel], min_dist, \
                    vehicle.max_brake, vehicle.t_react)
                print "needed_gap is %.1f" % needed_gap

                delta_t = 2. * (gap - needed_gap) / relative_speed
                acc_adj = relative_speed / delta_t
                if acc_adj > 2.0 or gap < 10:
                    if acc_adj > vehicle.max_brake:
                        acc_adj = vehicle.max_brake
                        print "remmen!"

                    else:
                        print "hij gaat zijn snelheid aanpassen met %.1f m/s2" % \
                            (-acc_adj)
                    new_speed = vehicle.speed[1] - acc_adj
                    vehicle.set_next_speed(new_speed)
                else:
                    print "hij gaat versnellen (t = %.1f, a was %.1f m/s2)" % \
                        (delta_t, -acc_adj)
                    vehicle.accelerate(self.max_speed, timedelta)

            else:
                vehicle.accelerate(self.max_speed, timedelta)
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
