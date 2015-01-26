import math
import matplotlib.pyplot as plt


class Edge:
    marge = 1.0
    max_count_accident = 10
    wall_marge = 1200

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

    def change_lanes(self):
        for vehicle in self.to_change:
            crashed = False
            self.to_change.remove(vehicle)

            if vehicle in self.collisions:
                crashed = True

            if(vehicle in self.vehicles):
                self.vehicles.remove(vehicle)

                direction = vehicle.change_lane.pop(0)
                if(direction == 'inner'):
                    self.inner_edge.add_vehicle(vehicle)
                elif(direction == 'outer'):
                    i = self.outer_edge.add_vehicle(vehicle)
                    self.outer_edge.move_vehicle(vehicle, i)
                else:
                    print "None made it here"

                if crashed:
                    self.collisions.remove(vehicle)
                    append_coll = ('self.' + direction + 
                        '_edge.collisions.append(vehicle)')
                    exec(append_coll)

    def vehicle_changes_lane(self, vehicle, side):
        if(len(vehicle.change_lane) == 0):
            vehicle.change_lane = [None] * int(round(vehicle.t_react /
                                                     self.timedelta, 0))
            vehicle.change_lane.insert(0, side)

    def stay_here(self, vehicle):
        try:
            this_edge = self.outer_edge

        # vehicle is already at the far right lane
        except AttributeError:
            return False

        # stay at this lane is there is a slower vehicle to the right
        interval = vehicle.location, vehicle.location + 50
        for veh in this_edge.vehicles:
            if (interval[0] < veh.location < interval[1]):
                if veh.speed < vehicle.speed:
                    return True

        # not necessary to stay at this lane
        return False

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
            if vehicle.max_acc(vehicle.speed, vehicle.mass) > 0:
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

        # use the extra option is there is no need to brake
        vehicle.use_extra = False

        # end of the lane reached
        if vehicle.location > self.edgesize:
            self.to_remove.append(vehicle)
            return 

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
            marge = vehicle_infront.length + self.marge

            # find the gap
            gap = vehicle_infront.location - vehicle.location
            min_gap = find_min_gap(current_speed, vehicle, marge)
            needed_gap = find_min_gap(vel0, vehicle, marge)

            '''
            Check for collision
            '''
            if self.collision_check(i):
                return

            # no collision: save the new place and speed
            vehicle.loc_speed_old = (vehicle.location, vehicle.speed)

            """
            Check if vehicle is within marge to wall
            """
            if(self.within_marge_to_wall(vehicle.location)):
                vehicle.wants_to_go_right = True
                if self.check_lane(vehicle, 'outer'):
                    self.vehicle_changes_lane(vehicle, 'outer')
                    vehicle.wants_to_go_right = False
                    vehicle.accelerate(self.max_speed, 
                        vehicle.extra_acc_adj, timedelta)
                    return
            else:
                vehicle.wants_to_go_right = False

            '''
            Check if it's possible to change lanes outward.
            '''
            if not self.stay_here(vehicle):
                if self.check_lane(vehicle, 'outer'):
                    self.vehicle_changes_lane(vehicle, 'outer')
                    vehicle.accelerate(self.max_speed, 
                        vehicle.extra_acc_adj, timedelta)
                    return
                else:
                    self.use_extra = False

            '''
            Driving too close to the vehicle in front
            '''
            if gap < min_gap:
                if self.check_lane(vehicle, 'inner'):
                    self.vehicle_changes_lane(vehicle, 'inner')
                    vehicle.accelerate(self.max_speed, 
                        vehicle.extra_acc_adj, timedelta)
                    return

                # adjust the speed in a way that:
                # next gap = current min_gap
                new_speed = 2. * (gap - min_gap) + 2. * vel0 - current_speed

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
                    for veh in this_edge.vehicles:
                        distance = find_min_gap(current_speed, vehicle, 
                            veh.length + self.marge, True)
                        marge = (vehicle.location + veh.length, 
                            vehicle.location + distance)

                        if (marge[0] < veh.location < marge[1] and
                            veh.wants_to_go_right and
                            -2. < vehicle.speed - veh.speed < 12.):

                            vehicle.extra_acc_adj = -2
                            vehicle.use_extra = True                            
                            
            except:
                # there is no inner edge (vehicle is at far left lane)
                AttributeError

            '''
            Driving the same speed as the vehicle in front
            '''
            if abs(relative_speed) < 0.5:
                # there is enough space to accelerate
                if gap > min_gap + vehicle.max_acc(vehicle.speed, vehicle.mass) \
                    * timedelta * timedelta:
                    
                    vehicle.accelerate(self.max_speed, 
                        vehicle.max_acc(vehicle.speed, vehicle.mass), timedelta)

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
                    acc_adj = vehicle.max_acc(vehicle.speed, vehicle.mass)

                vehicle.accelerate(self.max_speed, acc_adj, timedelta)
                return

            '''
            Driving faster than the vehicle in front
            '''
            # be aware that the vehicle in an accident will stop
            if vehicle_infront in self.collisions:
                relative_speed = current_speed

            # delta_t is nonzero, because if gap = needed_gap and 
            # drives too fast, the gap is less than min_gap
            delta_t = 2. * (gap - needed_gap) / relative_speed
            acc_adj = relative_speed / delta_t

            # If you need to brake more than -4.0 ms^2 try and change
            # lanes inward
            if (acc_adj > 5.0):
                # check lanes if possible
                if self.check_lane(vehicle, 'inner'):
                    self.vehicle_changes_lane(vehicle, 'inner')
                    vehicle.accelerate(self.max_speed, 
                        vehicle.extra_acc_adj, timedelta)
                    return

            # make an appropriate deceleration
            if (acc_adj > 2.0 or gap < 2 * needed_gap):
                # decelerate in current lane
                vehicle.accelerate(self.max_speed, -acc_adj, timedelta)

            # accelerate if the car in front is far away
            else:
                vehicle.accelerate(self.max_speed, 
                    vehicle.max_acc(vehicle.speed, vehicle.mass), timedelta)
        else:
                # accelerate
                vehicle.accelerate(self.max_speed, 
                    vehicle.max_acc(vehicle.speed, vehicle.mass), timedelta)

    '''
    Check if it's possible to change lanes.
    '''
    def check_lane(self, vehicle, side):
        loc0, speed0, len0 = vehicle.location, vehicle.speed, vehicle.length

        # changing to inner or outer lane
        try:
            if side == 'inner':
                this_edge = self.inner_edge

            elif side == 'outer':
                this_edge = self.outer_edge

        # there exists no such lane
        except AttributeError:
            return False

        # don't change to a lane with a wall near by
        if this_edge.within_marge_to_wall(loc0):
            return False

        '''
        There is a new acceleration that should be used if the vehicle
        wants to go right. It is only used if the vehicle does not have
        to slow down because of the vehicle in front of it
        '''
        num = len(this_edge.vehicles)
        vehicle.use_extra = True

        # return True if the lane is empty
        if num == 0:
            vehicle.extra_acc_adj = vehicle.max_acc(vehicle.speed, vehicle.mass)
            return True

        # there is only one car
        elif num == 1:
            first = this_edge.vehicles[0]
            second = first

        # find the two consecutive cars that are closest to vehicle
        else:
            index = 0
            first = this_edge.vehicles[index]
            second = this_edge.vehicles[index + 1]
            while second.location > loc0:
                index += 1
                if index + 1 < num:
                    first = this_edge.vehicles[index]
                    second = this_edge.vehicles[index + 1]
                else:
                    break

        loc_first, loc_second = first.location, second.location

        # both cars are behind vehicle
        if loc_first < loc0:
            gap_first = find_min_gap(first.speed, first, 
                len0 + self.marge, True)
            vehicle.extra_acc_adj = 3.
            if loc_first < loc0 < loc_first + gap_first:
                return False
            else:
                return True

        # both cars are in front of vehicle
        elif loc_second > loc0:
            gap_self = find_min_gap(speed0, vehicle, 
                second.length + self.marge, True)
            if loc0 < loc_second < loc0 + gap_self:
                vehicle.extra_acc_adj = -3.
                return False
            else:
                vehicle.extra_acc_adj = (second.speed - speed0)
                return True

        # vehicle's location is in between these cars
        else:
            gap_self = find_min_gap(speed0, vehicle, 
                first.length + self.marge, True)
            gap_second = find_min_gap(second.speed, second, 
                len0 + self.marge, True)

            if (loc_second < loc0 < loc_second + gap_second) or \
                (loc0 < loc_first < loc0 + gap_self):

                if (loc_second < loc0 < loc_second + gap_second):
                    acc_adj = 3.
                else:
                    acc_adj = -3.
                vehicle.extra_acc_adj = acc_adj
                return False
            else:
                acc_adj = (first.speed - speed0)
                vehicle.extra_acc_adj = acc_adj
                return True

    def within_marge_to_wall(self, location):
        try:
            marge = self.walls[0][0] - self.wall_marge, self.walls[0][1]
            if marge[0] < location < marge[1]:
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
                veh.wants_to_go_right = False
                veh.use_extra = False

        return collision


def find_min_gap(v_current, vehicle, marge, reactiontime = False):
    t_brake_abs = v_current / vehicle.max_brake
    x_brake_abs = (v_current * t_brake_abs) / 2.
    gap = x_brake_abs + marge
    if reactiontime:
        gap += vehicle.t_react * v_current
    return gap
