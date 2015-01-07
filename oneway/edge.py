from vehicle import Vehicle
import matplotlib.pyplot as plt


class Edge:
    vehicles = []
    max_speed = 40
    marge = 0.5

    def __init__(self, edgesize):
        self.id = id
        self.edgesize = edgesize

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
            print "auto %d begint op locatie" % i, vehicle.location,\
                "met snelheid", vehicle.speed[0]
            new_location = vehicle.location + timedelta * 0.5 * (vehicle.speed[0] +
                                                             vehicle.speed[1])
            print "rijdt naar ", new_location, "met eindsnelheid", vehicle.speed[1]
            vehicle.location = new_location

            if(i is not 0):
                # find gap
                vehicle_infront = self.vehicles[i - 1]
                relative_speed = vehicle.speed[1] - vehicle_infront.speed[0]
                if relative_speed < 0:
                    vehicle.accelerate(self.max_speed, timedelta)
                    continue

                print "Snelheid auto voor zich", vehicle_infront.speed[0]
                print "Relatieve snelheid", relative_speed
                t_brake_rel = relative_speed / vehicle.max_brake
                #x_brake_rel = t_brake_rel * (vehicle_infront.speed[0] +
                 #                            0.5 * relative_speed)
                t_brake_abs = vehicle.speed[0] / vehicle.max_brake
                x_brake_abs = (vehicle.speed[0] * t_brake_abs) / 2.
                gap = vehicle_infront.location - vehicle.location
                print "Gat is", gap, "remafstand is", x_brake_abs
                if gap < 0:
                    print "FATAL ERROR!!! >:( "

                # decide to brake
                min_gap = x_brake_abs + vehicle.t_react * (vehicle.speed[0] +
                                                       vehicle.speed[1]) / 2.

                if gap <= min_gap:
                    print "hij gaat straks remmen"
                    new_speed = vehicle.speed[1] - vehicle.max_brake
                    if(new_speed < 0):
                        new_speed = 0
                    vehicle.set_next_speed(new_speed)
                else:
                    print "hij gaat harder rijden"
                    vehicle.accelerate(self.max_speed, timedelta)

            else:
                vehicle.accelerate(self.max_speed, timedelta)

            print "auto %d nu op positie" % i, vehicle.location, "met snelheid",\
                  vehicle.speed[0]
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
