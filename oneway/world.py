from car import Car
import matplotlib.pyplot as plt

class World:
    worldsize = 0
    cars = []
    max_speed = 15

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
            print "auto %d begint op locatie", car.location, "met snelheid", \
                  car.speed[0]
            new_location = car.location + timedelta * 0.5 * (car.speed[0] + \
                                                             car.speed[1])
            print "rijdt naar ", new_location
            car.location = new_location

            if(i is not 0):
                # find gap
                relative_speed = car.speed - self.cars[i - 1].speed
                t_brake = relative_speed / car.max_brake
                x_brake = t_brake * (self.cars[i - 1].speed + \
                                     0.5 * relative_speed)   
                gap = self.cars[i-1].location - car.location
                if gap < 0:
                    print "FATAL ERROR :( "

                # decide to brake
                if(gap <= x_brake):
                    print "hij gaat straks remmen"
                    new_speed = car.speed - car.max_brake
                    if(new_speed < 0):
                        new_speed = 0
                    car.set_next_speed(new_speed)
                else:
                    print "hij gaat harder rijden"
                    car.accellerate(max_speed, timedelta)
                    
            else:
                car.accellerate(max_speed, timedelta)

            print "auto %d nu op positie", car.location, 

    def plot_cars(self):
        cars_xy = [[], []]
        for car in self.cars:
            cars_xy[0].append(car.location)
            cars_xy[1].append(1)
        plt.plot(cars_xy[0], cars_xy[1], 'o')
        plt.draw()
        plt.pause(0.3)
        plt.clf()
