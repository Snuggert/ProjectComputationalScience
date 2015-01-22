import math
import matplotlib.pyplot as plt


class Edge:
    marge = 1.0
    max_count_accident = 10
    wall_marge = 600

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
        self.to_change = []
        self.walls = []

    def add_vehicle(self, vehicle, remove=False):
        if(remove):
            self.remove_vehicle_from_neigbors(vehicle)

        if(len(self.vehicles) == 0):
            self.vehicles.append(vehicle)
            return 0
        index = 0
        while True:
            if(index >= len(self.vehicles) or
               vehicle.location > self.vehicles[index].location):
                self.vehicles.insert(index, vehicle)
                return index
            index += 1

    def add_neighbor(self, edge, inner):
        if inner:
            self.inner_edge = edge
        else:
            self.outer_edge = edge

    def add_wall(self, up_lim, low_lim):
        self.walls.append([up_lim, low_lim])

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
        if(max_loc > self.edgesize or min_loc > self.edgesize):
            return False
        if(self.within_marge_to_wall(max_loc) or self.within_marge_to_wall(min_loc)):
            return False
        for vehicle in self.vehicles:
            if max_loc > vehicle.location > min_loc:
                return False
            try:
                x = (self.start_wall - self.wall_marge, self.stop_wall)
                if x[0] < max_loc < x[1]:
                    return False
            except:
                AttributeError

        return True

    def change_lanes(self):
        for vehicle in self.to_change:
            self.to_change.remove(vehicle)

            if(vehicle in self.vehicles):
                self.vehicles.remove(vehicle)
                direction = vehicle.change_lane.pop(0)
                if(direction == 'inward'):
                    self.inner_edge.add_vehicle(vehicle)
                elif(direction == 'outward'):
                    i = self.outer_edge.add_vehicle(vehicle)
                    self.outer_edge.move_vehicle(vehicle, i)
                else:
                    print "None made it here"

    def move_vehicles(self):
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
            if vehicle.max_acc(vehicle.speed) > 0:
                self.move_vehicle(vehicle, i)

    def move_vehicle(self, vehicle, i):
        timedelta = self.timedelta
        '''
        Check if vehicle wants to change lane next tick.
        '''
        if(len(vehicle.change_lane) > 0):
            direction = vehicle.change_lane[0]
            if(direction is not None):
                self.to_change.append(vehicle)
            else:
                vehicle.change_lane.pop(0)

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
                    return

            if self.collision_check(i):
                return

            vehicle.accelerate(self.max_speed, -vehicle.max_brake,
                               timedelta)
            return

        """Check if vehicle is within marge to wall"""
        if(self.within_marge_to_wall(vehicle.location)):
            vehicle.wants_to_go_right = True
            if(self.check_lane(vehicle, 20, 30, 'outer')):
                if(len(vehicle.change_lane) == 0):
                    vehicle.change_lane = [None] * int(round(vehicle.t_react /
                                                             timedelta, 0))
                    vehicle.change_lane.insert(0, 'outward')
                    vehicle.wants_to_go_right = False
            else:
                vehicle.accelerate(self.max_speed, -2.0, timedelta)

        # Make a decision for each vehicle (that is not in front or in an
        # accident).
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
                return

            # no collision: save the new place and speed
            vehicle.loc_speed_old = (vehicle.location, vehicle.speed)

            '''
            Check if it's possible to change lanes outward.
            '''
            if(self.check_lane(vehicle, 20, 50, 'outer')):
                if(len(vehicle.change_lane) == 0):
                    vehicle.change_lane = [None] * int(round(vehicle.t_react /
                                                             timedelta, 0))
                    vehicle.change_lane.insert(0, 'outward')

            '''
            Driving too close to the vehicle in front
            '''
            if gap < min_gap:
                if(self.check_lane(vehicle, 50, 20, 'inner') and
                   len(vehicle.change_lane) == 0):
                        vehicle.change_lane = [None] * int(round(vehicle.t_react /
                                                                 timedelta, 0))
                        vehicle.change_lane.insert(0, 'inward')

                # adjust the speed in a way that:
                # next gap = current min_gap
                new_speed = 2. / timedelta * (gap - min_gap) + 2. * vel0 -\
                    current_speed

                acc_adj = min([new_speed - current_speed, 0])

                vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                return

            '''
            The vehicle to the left wants to go right
            '''
            try:
                this_edge = self.inner_edge
                num = len(this_edge.vehicles)
                if num > 0:
                    # find the car at the (front) left that is closest
                    k = num - 1
                    left_vehicle = this_edge[k]
                    while left_vehicle.location < vehicle.location:
                        k -= 1
                        if k < 0:
                            break
                        left_vehicle = this_edge[k]

                    # vehicle front left found
                    if k >= 0:
                        if left_vehicle.wants_to_go_right:
                            delta = left_vehicle.location - vehicle.location

                            # decelerate if the vehicle is close enough
                            if delta > 0 and delta < 30 and delta < gap:
                                vehicle.accelerate(self.max_speed, -4,
                                                   timedelta)
                                return
            except:
                # there is no inner edge (vehicle is at far left lane)
                AttributeError

            '''
            Driving the same speed as the vehicle in front
            '''
            if abs(relative_speed) < 0.5:
                # there is enough space to accelerate
                if gap > min_gap + vehicle.max_acc(vehicle.speed) * timedelta * timedelta:
                    vehicle.accelerate(self.max_speed, vehicle.max_acc(vehicle.speed),
                                       timedelta)

                # take the speed of the vehicle in front
                else:
                    acc_adj = vel0 - current_speed
                    vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                return

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
                    acc_adj = vehicle.max_acc(vehicle.speed)

                vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                return

            '''
            Driving faster than the vehicle in front
            '''
            # be aware that the vehicle in an accident will stop
            if vehicle_infront in self.collisions:
                relative_speed = current_speed

            delta_t = 2. * (gap - needed_gap) / relative_speed
            acc_adj = relative_speed / delta_t

            # If you need to brake more than -4.0 ms^2 try and change
            # lanes inward
            if (acc_adj > 5.0):
                # check lanes if possible
                if(self.check_lane(vehicle, 50, 20, 'inner') and
                        len(vehicle.change_lane) == 0):
                    vehicle.change_lane = [None] * int(round(vehicle.t_react /
                                                             timedelta, 0))
                    vehicle.change_lane.insert(0, 'inward')
                    vehicle.accelerate(self.max_speed, 0, timedelta)
                    return

            # make an appropriate deceleration
            if (acc_adj > 2.0 or gap < 2 * needed_gap):
                # decelerate in current lane
                vehicle.accelerate(self.max_speed, -acc_adj, timedelta)

            # accelerate if the car in front is far away
            else:
                vehicle.accelerate(self.max_speed, vehicle.max_acc(vehicle.speed),
                                   timedelta)
        else:
                # accelerate
                vehicle.accelerate(self.max_speed, vehicle.max_acc(vehicle.speed), timedelta)

    '''
    Check if it's possible to change lanes.
    '''
    def check_lane(self, vehicle, margin_backward, margin_forward, side):
        try:
            if(side == 'inner'):
                if(self.inner_edge.check_location(
                    vehicle.location - margin_backward,
                        vehicle.location + margin_forward)):
                    return True
            elif(side == 'outer'):
                if(self.outer_edge.check_location(
                    vehicle.location - margin_backward,
                        vehicle.location + margin_forward)):
                    return True
        except AttributeError:
            return False
        return False

    def within_marge_to_wall(self, location):
        try:
            diff = self.walls[0][0] - location
            if(0 < diff < self.wall_marge):
                return True
        except IndexError:
            return False
        return False

    def plot_vehicles(self, x1, x2):
        edge = self
        lane = 1

        while True:
            vehicles_xy = [[], []]
            for vehicle in edge.vehicles:
                vehicles_xy[0].append(vehicle.location)
                vehicles_xy[1].append(lane)
            plt.plot(vehicles_xy[0], vehicles_xy[1], 'gs')

            collision_xy = [[], []]
            for vehicle in edge.collisions:
                collision_xy[0].append(vehicle.location)
                collision_xy[1].append(lane)
            plt.plot(collision_xy[0], collision_xy[1], 'rs')
            eps = 0.4
            plt.axhspan(lane - eps, lane + eps, facecolor="black",
                        alpha=0.3)
            lane += 1
            try:
                edge = edge.inner_edge
            except AttributeError:
                break

        plt.axis([x1, x2, -5, lane + 5])
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
            if vehicle not in self.collisions:
                print "FATAL ERROR!!! >:( "
                print "auto %d botst op voorganger op locatie %.1f" % (i,
                                                                       vehicle.location)

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
