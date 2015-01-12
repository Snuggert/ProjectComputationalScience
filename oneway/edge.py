import math
import matplotlib.pyplot as plt

class Edge:
    marge = 1.0
    max_count_accident = 10

    def __init__(self, locations, max_speed, tick):
        self.id = id
        self.locations = locations
        self.edgesize = \
            math.sqrt(math.pow(locations[1][0] - locations[0][0], 2) +
                      math.pow(locations[1][1] - locations[0][1], 2))
        self.max_speed = max_speed
        self.timedelta = tick
        self.vehicles = []
        self.to_remove = []
        self.collisions = []

    def move_vehicles(self):
        # remove vehicles
        timedelta = self.timedelta

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def move_vehicles(self, timedelta):
        # remove vehicles
        for vehicle in self.to_remove:
            if vehicle in self.vehicles:
                self.vehicles.remove(vehicle)
            self.to_remove.remove(vehicle)


    def move_vehicles(self, timedelta):
        # remove vehicles
        for vehicle in self.to_remove:
            if vehicle in self.vehicles:
                self.vehicles.remove(vehicle)
            self.to_remove.remove(vehicle)

        # return if empty
        if(len(self.vehicles) == 0):
            return

        # move each vehicle and make decisions
        for i, vehicle in enumerate(self.vehicles):
            '''
            Move vehicle
            '''

            # start situation
            begin = vehicle.location, vehicle.speed[0]

            # new situation
            current_speed = vehicle.speed[1]
            vehicle.location = vehicle.location + timedelta * 0.5 * \
                (vehicle.speed[0] + current_speed)

            # end of the lane reached
            if vehicle.location > self.edgesize:
                self.to_remove.append(vehicle)

            # vehicle was in an accident
            if vehicle in self.collisions:
                if abs(current_speed) < 0.01:
                    vehicle.count_to_remove += 1
                    if vehicle.count_to_remove >= int(self.max_count_accident /
                                                      timedelta):
                        self.to_remove.append(vehicle)
                        continue

                next_speed = current_speed - vehicle.max_brake
                vehicle.set_next_speed(next_speed)
                continue

            # Make a decision for each vehicle (that is not in front or in an
            # accident.
            if(i is not 0):
                '''
                Find the gap and other constants
                '''
                # observe vehicle in front
                vehicle_infront = self.vehicles[i - 1]
                vel0 = vehicle_infront.speed[0]
                relative_speed = current_speed - vel0

                # find parameters for this vehicle
                min_dist = vehicle_infront.length + self.marge
                params = min_dist, vehicle.max_brake, vehicle.t_react

                # find the gap
                gap = vehicle_infront.location - vehicle.location
                min_gap = find_min_gap(current_speed, params)
                needed_gap = find_min_gap(vel0, params)

                '''
                Check for collision
                '''
                if gap < vehicle_infront.length:
                    print "FATAL ERROR!!! >:( "

                    # new location vehicle
                    vehicle.location = (vehicle_infront.location
                                        - vehicle_infront.length)
                    loc0, v0 = begin
                    dx = (vehicle_infront.location - vehicle_infront.length
                          - loc0)

                    # find the velocity at which the vehicle clashed
                    a = current_speed - v0
                    if abs(a) < 0.01:
                        v_coll = v0
                    else:
                        D = v0 * v0 + 2 * a * dx
                        dt = (- v0 + math.sqrt(D)) / a
                        v_coll = v0 + a * dt

                    # find the new velocity at which they both move
                    m1, m2 = vehicle.mass, vehicle_infront.mass
                    avg_speed = (m1* v_coll + m2 * vel0) / (m1 + m2)

                    # find the maximum deceleration for the clashed vehicles
                    a1, a2 = vehicle.max_brake, vehicle_infront.max_brake
                    if a1 < a2:
                        avg_max_brake = (m1 * a1 + m2 * a2) / (m1 + m2)
                        vehicle.max_brake = avg_max_brake
                        vehicle_infront.max_brake = avg_max_brake

                    # append to the list of collisions
                    for veh in [vehicle, vehicle_infront]:
                        veh.speed[1] = avg_speed
                        veh.set_next_speed(avg_speed - veh.max_brake)

                        if veh not in self.collisions:
                            self.collisions.append(veh)
                        veh.count_to_remove = 0
                    continue

                '''
                Driving too close to the vehicle in front
                '''
                if gap < min_gap:
                    # adjust the speed in a way that: next gap = current min_gap
                    new_speed = 2. / timedelta * (gap - min_gap) + 2. * vel0 - current_speed
                    acc_adj = new_speed - current_speed
                    if acc_adj < - vehicle.max_brake:
                        acc_adj = - vehicle.max_brake
                    # don't accelerate
                    elif acc_adj > 0:
                        acc_adj = 0

                    new_speed = current_speed + acc_adj
                    vehicle.set_next_speed(new_speed)
                    continue

                '''
                Driving the same speed as the vehicle in front
                '''
                if abs(relative_speed) < 0.5:
                    # there is enough space to accelerate
                    if gap > min_gap + vehicle.max_acc * timedelta * timedelta:
                        vehicle.accelerate(self.max_speed, vehicle.max_acc, timedelta)

                    # take the speed of the vehicle in front
                    else:
                        vehicle.set_next_speed(vel0)
                    continue

                '''
                Driving slower than the vehicle in front
                '''
                if relative_speed < 0:
                    # make an appropriate acceleration
                    if gap < needed_gap:
                        delta_t = 2. * (needed_gap - gap) / (-relative_speed)
                        acc_adj = (-relative_speed) / delta_t
                        if acc_adj > vehicle.max_acc:
                            acc_adj = vehicle.max_acc
                            (acc_adj, delta_t)
                    # maximal acceleration
                    else:
                        acc_adj = vehicle.max_acc

                    vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                    continue

                '''
                Driving faster than the vehicle in front
                '''
                delta_t = 2. * (gap - needed_gap) / relative_speed
                acc_adj = relative_speed / delta_t
                # make an appropriate deceleration
                if (acc_adj > 2.0 or gap < 2 * needed_gap):
                    new_speed = current_speed - acc_adj
                    acc_adj = current_speed - new_speed
                    if acc_adj > vehicle.max_brake:
                        acc_adj = vehicle.max_brake
                        (-acc_adj)
                    vehicle.set_next_speed(new_speed)

                # accelerate if the car in front is far away
                else:
                    vehicle.accelerate(self.max_speed, vehicle.max_acc, timedelta)

            else:
                # accelerate
                vehicle.accelerate(self.max_speed, vehicle.max_acc,timedelta)


    def plot_vehicles(self):
        vehicles_xy = [[], []]
        for vehicle in self.vehicles:
            vehicles_xy[0].append(vehicle.location)
            vehicles_xy[1].append(1)
        plt.plot(vehicles_xy[0], vehicles_xy[1], 'bs')

        collision_xy = [[], []]
        for vehicle in self.collisions:
            collision_xy[0].append(vehicle.location)
            collision_xy[1].append(1)
        plt.plot(collision_xy[0], collision_xy[1], 'rs')
        plt.axis([0, self.edgesize, 0, 2])
        plt.draw()
        plt.pause(0.001)
        plt.clf()

def find_min_gap(v_current, params):
    min_dist, max_brake, t_react = params
    t_brake_abs = v_current / max_brake
    x_brake_abs = (v_current * t_brake_abs) / 2.
    gap = x_brake_abs + min_dist
    return gap