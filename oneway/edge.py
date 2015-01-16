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

    def add_vehicle(self, vehicle, remove=False):
        if(remove):
            self.remove_vehicle_from_neigbors(vehicle)

        if(len(self.vehicles) == 0):
            self.vehicles.append(vehicle)
            return 0
        index = 0
        while True:
            if(index == len(self.vehicles) or
               vehicle.location > self.vehicles[index].location):
                self.vehicles.insert(index, vehicle)
                return index
            index += 1

    def add_neighbor(self, edge, inner):
        if self.edgesize == edge.edgesize:
            if inner:
                self.inner_edge = edge
            else:
                self.outer_edge = edge
        else:
            return 0

    def remove_vehicle_from_neigbors(self, vehicle):
        try:
            self.inner_edge.vehicles.remove(vehicle)
        except AttributeError:
            pass
        except ValueError:
            pass
        try:
            self.outer_edge.vehicles.remove(vehicle)
        except AttributeError:
            pass
        except ValueError:
            pass

    def check_location(self, min_loc, max_loc):
        for vehicle in self.vehicles:
            if(max_loc > vehicle.location > min_loc):
                return False
        return True

    def move_vehicles(self):
        timedelta = self.timedelta

        # remove vehicles
        for vehicle in self.to_remove:
            if vehicle in self.vehicles:
                self.vehicles.remove(vehicle)
            if vehicle in self.collisions:
                self.collisions.remove(vehicle)
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
            old_loc, old_speed = vehicle.loc_speed_old

            # new situation
            current_speed = vehicle.speed
            vehicle.location = vehicle.location + timedelta * 0.5 * \
                (old_speed + current_speed)

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
                        print "auto wordt weggesleept"
                        continue

                if self.collision_check(i):
                    continue

                vehicle.accelerate(self.max_speed, -vehicle.max_brake,
                                   timedelta)
                continue

            # Make a decision for each vehicle (that is not in front or in an
            # accident.
            if(i is not 0):
                '''
                Find the gap and other constants
                '''
                # observe vehicle in front
                vehicle_infront = self.vehicles[i - 1]
                vel0 = vehicle_infront.speed
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
                if self.collision_check(i):
                    continue

                # no collision: save the new place and speed
                vehicle.loc_speed_old = (vehicle.location, vehicle.speed)

                '''
                Check if it's possible to change lanes outward.
                '''
                if(self.check_outward(vehicle)):
                    index = self.outer_edge.add_vehicle(vehicle, True)
                    if index == 0:
                        vehicle.accelerate(self.max_speed,
                                           vehicle.max_acc,
                                           timedelta)
                        continue
                    # observe vehicle in front
                    vehicle_infront = self.outer_edge.vehicles[index - 1]
                    vel0 = vehicle_infront.speed
                    relative_speed = current_speed - vel0

                    # find parameters for this vehicle
                    min_dist = vehicle_infront.length + self.marge
                    params = min_dist, vehicle.max_brake, vehicle.t_react

                    # find the gap
                    gap = vehicle_infront.location - vehicle.location
                    min_gap = find_min_gap(current_speed, params)
                    needed_gap = find_min_gap(vel0, params)

                '''
                Driving too close to the vehicle in front
                '''
                if gap < min_gap:
                    if(self.check_inward(vehicle)):
                        self.inner_edge.add_vehicle(vehicle, True)
                        vehicle.accelerate(self.inner_edge.max_speed,
                                           vehicle.max_acc,
                                           self.inner_edge.timedelta)
                        continue

                    # adjust the speed in a way that:
                    # next gap = current min_gap
                    new_speed = 2. / timedelta * (gap - min_gap) + 2. * vel0 -\
                        current_speed

                    acc_adj = new_speed - current_speed

                    # don't accelerate
                    if acc_adj > 0:
                        acc_adj = 0

                    vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                    continue

                '''
                Driving the same speed as the vehicle in front
                '''
                if abs(relative_speed) < 0.5:
                    # there is enough space to accelerate
                    if gap > min_gap + vehicle.max_acc * timedelta * timedelta:
                        vehicle.accelerate(self.max_speed, vehicle.max_acc,
                                           timedelta)

                    # take the speed of the vehicle in front
                    else:
                        acc_adj = vel0 - current_speed
                        vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                    continue

                '''
                Driving slower than the vehicle in front
                '''
                if relative_speed < 0:
                    # make an appropriate acceleration
                    if gap < needed_gap:
                        delta_t = 2. * (needed_gap - gap) / (-relative_speed)
                        acc_adj = (-relative_speed) / delta_t

                    # maximal acceleration
                    else:
                        acc_adj = vehicle.max_acc

                    vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                    continue

                '''
                Driving faster than the vehicle in front
                '''
                # be aware that the vehicle in an accident will stop
                if vehicle_infront in self.collisions:
                    relative_speed = current_speed

                delta_t = 2. * (gap - needed_gap) / relative_speed
                acc_adj = relative_speed / delta_t

                # make an appropriate deceleration or change lanes
                if (acc_adj > 2.0 or gap < 2 * needed_gap):

                    # check lanes if possible
                    if(self.check_outward(vehicle)):
                        self.inner_edge.add_vehicle(vehicle, True)
                        vehicle.accelerate(self.inner_edge.max_speed,
                                           vehicle.max_acc,
                                           self.inner_edge.timedelta)
                        continue

                    # decelerate in current lane
                    vehicle.accelerate(self.max_speed, -acc_adj, timedelta)

                # accelerate if the car in front is far away
                else:
                    vehicle.accelerate(self.max_speed, vehicle.max_acc,
                                       timedelta)

            else:
                # accelerate
                vehicle.accelerate(self.max_speed, vehicle.max_acc, timedelta)

    '''
    Check if it's possible to change lanes outward.
    '''
    def check_outward(self, vehicle):
        try:
            if(self.outer_edge.check_location(vehicle.location - 15.,
                                              vehicle.location + 30)):
                return True
        except AttributeError:
            return False
        return False

    def check_inward(self, vehicle):
        try:
            if(self.inner_edge.check_location(vehicle.location - 30.,
                                              vehicle.location + 10)):
                return True
        except AttributeError:
            return False
        return False

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
        plt.pause(0.00001)
        plt.clf()

    def collision_check(self, i):
        timedelta = self.timedelta
        if i == 0:
            return False

        vehicle = self.vehicles[i]
        vehicle_infront = self.vehicles[i - 1]
        gap = vehicle_infront.location - vehicle.location
        
        collision = False

        if gap < vehicle_infront.length:
            collision = True
            print "FATAL ERROR!!! >:( "
            print "auto %d botst op voorganger" % i

            # new location vehicle
            vehicle.location = (vehicle_infront.location
                                - vehicle_infront.length - 0.01)

            loc0, v0 = vehicle.loc_speed_old
            current_speed, vel0 = vehicle.speed, vehicle_infront.speed

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
            avg_speed = (m1 * v_coll + m2 * vel0) / (m1 + m2)

            # append to the list of collisions
            for veh in [vehicle, vehicle_infront]:
                veh.accelerate(self.max_speed, -vehicle.max_brake, timedelta)

                if veh not in self.collisions:
                    self.collisions.append(veh)

                # adjust variables
                veh.count_to_remove = 0
                veh.loc_speed_old = veh.location, avg_speed
                veh.speed = avg_speed


        return collision


def find_min_gap(v_current, params):
    min_dist, max_brake, t_react = params
    t_brake_abs = v_current / max_brake
    x_brake_abs = (v_current * t_brake_abs) / 2.
    gap = x_brake_abs + min_dist
    return gap
