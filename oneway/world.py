from car import Car


class World:
    worldsize = 0
    cars = []
    max_speed = 15

    def __init__(self, worldsize):
        self.id = id
        self.worldsize = worldsize

    def add_car(self, speed, location):
        self.cars.append(Car(speed, location))

    def move_cars(self):
        for i, car in enumerate(self.cars):
            t_brake = car.speed / car.max_brake
            x_brake = car.speed * t_brake - (car.max_brake * t_brake * t_brake) / 2
            try:
                if(self.cars[i-1].location - car.location <= x_brake):
                    new_speed = car.speed - car.max_brake
                    if(new_speed < 0):
                        new_speed = 0
                    car.set_next_speed(new_speed)
            except ValueError, e:
                raise
