from car import Car
import matplotlib.pyplot as plt

class World:
    worldsize = 0
    cars = []
    max_speed = 15

    def __init__(self, worldsize):
        self.id = id
        self.worldsize = worldsize

    def add_car(self, speed, location):
        self.cars.append(Car(speed, location))

    def move_cars(self, timedelta):
        for i, car in enumerate(self.cars):
            new_location = timedelta * car.speed + car.location
            try:
                if(new_location > ):
                    car.location = timedelta * car.speed + car.location

                relative_speed = car.speed - self.cars[i - 1].speed
                t_brake = relative_speed / car.max_brake
                x_brake = t_brake * (self.cars[i - 1].speed + 0.5 * relative_speed)
                if(self.cars[i-1].location - car.location <= x_brake):
                    new_speed = car.speed - car.max_brake
                    if(new_speed < 0):
                        new_speed = 0
                    car.set_next_speed(new_speed)
            except ValueError, e:
                car.location =  timedelta * car.speed + car.location
                car.speed = car.speed + car.max_accellerate

    def plot_cars(self):
        cars_xy = [[], []]
        for car in self.cars:
            cars_xy[0].append(car.location)
            cars_xy[1].append(1)
        plt.plot(cars_xy[0], cars_xy[1], 'o')
        plt.draw()
        plt.pause(0.3)
        plt.clf()
