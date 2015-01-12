import math
import matplotlib.pyplot as plt


class Edge:
    max_speed = 30
    marge = 1.0

    def __init__(self, locations):
        self.id = id
        self.vehicles = []
        self.locations = locations
        self.edgesize = int(math.sqrt(
            math.pow(locations[1][0] - locations[0][0], 2) +
            math.pow(locations[1][1] - locations[0][1], 2)) + 0.5)

    def add_neighbor(self, edge, inner):
        if self.edgesize == edge.edgesize:
            if inner:
                self.inner_edge = edge
            else:
                self.outer_edge = edge
        else:
            return 0

    def add_vehicle(self, vehicle, remove=False):
        if(remove):
            self.remove_vehicle_from_neigbors(vehicle)

        if(len(self.vehicles) == 0):
            self.vehicles.append(vehicle)
            return
        index = 0
        while True:
            if(index == len(self.vehicles) or
               vehicle.location > self.vehicles[index].location):
                self.vehicles.insert(index, vehicle)
                return
            index += 1

    def check_location(self, min_loc, max_loc):
        for vehicle in self.vehicles:
            if(max_loc > vehicle.location > min_loc):
                return False
        return True

    def remove_vehicle_from_neigbors(self, vehicle):
        try:
            self.inner_edge.vehicles.remove(vehicle)
        except AttributeError:
            pass
        try:
            self.outer_edge.vehicles.remove(vehicle)
        except AttributeError:
            pass

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
            new_location = vehicle.location + timedelta * 0.5 * \
                (vehicle.speed[0] + vehicle.speed[1])
            current_speed = vehicle.speed[1]
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
                relative_speed = current_speed - vehicle_infront.speed[0]
                min_gap = find_min_gap(current_speed, params)

                '''
                Check for collision
                '''
                if gap < vehicle_infront.length:
                    print "FATAL ERROR!!! >:( "

                '''
                Driving too close to the vehicle in front
                '''
                if gap < min_gap:
                    new_speed = 2. / timedelta * (gap - min_gap) + 2. * vel0 \
                        - current_speed
                    acc_adj = new_speed - current_speed
                    if acc_adj < - vehicle.max_brake:
                        acc_adj = - vehicle.max_brake
                    try:
                        if(self.inner_edge.check_location(vehicle.location - 20, vehicle.location + 20)):
                            self.inner_edge.add_vehicle(vehicle, True)
                            vehicle.set_next_speed(current_speed +
                                                   vehicle.max_accelerate)
                    except AttributeError:
                        vehicle.set_next_speed(new_speed)
                    continue

                '''
                Driving the same speed as the vehicle in front
                '''
                if abs(relative_speed) < 0.5:
                    if gap > min_gap + vehicle.max_accelerate * \
                            timedelta * timedelta:
                        vehicle.accelerate(self.max_speed,
                                           vehicle.max_accelerate, timedelta)
                    else:
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
                            (acc_adj, delta_t)
                    else:
                        acc_adj = vehicle.max_accelerate

                    vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                    continue

                '''
                Driving faster than the vehicle in front
                '''
                delta_t = 2. * (gap - needed_gap) / relative_speed
                acc_adj = relative_speed / delta_t
                if (acc_adj > 1.0 or gap < 2 * needed_gap):
                    new_speed = current_speed - acc_adj
                    acc_adj = current_speed - new_speed
                    if acc_adj > vehicle.max_brake:
                        acc_adj = vehicle.max_brake
                        print "remmen!"
                    vehicle.set_next_speed(new_speed)
                else:
                    vehicle.accelerate(self.max_speed, vehicle.max_accelerate,
                                       timedelta)

            else:
                vehicle.accelerate(self.max_speed,
                                   vehicle.max_accelerate, timedelta)

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
