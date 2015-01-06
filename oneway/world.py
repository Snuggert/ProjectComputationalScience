from car import Car
import matplotlib.pyplot as plt


class World:
    worldsize = 0
    cars = []
    max_speed = 15
    marge = 0.5

    def __init__(self, worldsize):
        self.id = id
        self.worldsize = worldsize

    def add_car(self, speed, max_speed, location):
        self.cars.append(Car(speed, location))

    def move_cars(self, timedelta):
        car = self.cars[0]
        while car <= self.worldsize:
            self.cars.remove(car)
            car = self.cars[0]

        for i, car in enumerate(self.cars):
            print "auto %d begint op locatie" % i, car.location,\
                "met snelheid", car.speed[0]
            new_location = car.location + timedelta * 0.5 * (car.speed[0] +
                                                             car.speed[1])
            print "rijdt naar ", new_location, "met eindsnelheid", car.speed[1]
            car.location = new_location

            if(i is not 0):
                # find gap
                relative_speed = car.speed[1] - self.cars[i - 1].speed[0]
                if relative_speed < 0:
                    car.accellerate(self.max_speed, timedelta)
                    continue

                print "Snelheid auto voor zich", self.cars[i - 1].speed[0]
                print "Relatieve snelheid", relative_speed
                t_brake_rel = relative_speed / car.max_brake
                x_brake_rel = t_brake_rel * (self.cars[i - 1].speed[0] +
                                             0.5 * relative_speed)
                t_brake_abs = car.speed[0] / car.max_brake
                x_brake_abs = (car.speed[0] * t_brake_abs) / 2.
                gap = self.cars[i - 1].location - car.location
                print "Gat is", gap, "remafstand is", x_brake_abs
                if gap < 0:
                    print "FATAL ERROR :( "

                # decide to brake
                if(gap <= x_brake_rel + x_brake_abs +
                   car.t_react * (car.speed[0] + car.speed[1]) / 2.):
                    print "hij gaat straks remmen"
                    new_speed = car.speed[1] - car.max_brake
                    if(new_speed < 0):
                        new_speed = 0
                    car.set_next_speed(new_speed)
                else:
                    print "hij gaat harder rijden"
                    car.accellerate(self.max_speed, timedelta)

            else:
                car.accellerate(self.max_speed, timedelta)

            print "auto %d nu op positie" % i, car.location, "met snelheid",\
                  car.speed[0]
            print ""

    def plot_cars(self):
        cars_xy = [[], []]
        for car in self.cars:
            cars_xy[0].append(car.location)
            cars_xy[1].append(1)
        plt.plot(cars_xy[0], cars_xy[1], 'o')
        plt.axis([0, self.worldsize, 0.99, 1.01])
        plt.draw()
        plt.pause(0.2)
        plt.clf()
