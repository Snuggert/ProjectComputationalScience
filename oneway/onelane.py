import pygame
import sys
import simpy
import random

import matplotlib.pyplot as plt
from edge import Edge
from vehicle import Vehicle
from canvas import Canvas
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def max_speed(loc):
    return 600


def main():
    tick = 0.1
    my_canvas = Canvas()
    my_edge = Edge([[0, 100], [500, 100]], max_speed, tick)
    my_canvas.max_edge = my_edge.edgesize

    my_edge.add_vehicle(Vehicle(0., 400., 'broken', tick))
    for i in range(9, 2, -1):
        new_vehicle = Vehicle(random.randint(0, 10), i * 20., 'car', tick)
        my_edge.add_vehicle(new_vehicle)

    env = simpy.Environment()
    env.process(simulate(env, my_edge, tick, my_canvas))
    env.run(until=500)
    plt.show()


def simulate(env, edge, tick, my_canvas):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        my_canvas.clear_screen((10, 10, 12))
        my_canvas.draw_edge(edge)

        edge.move_vehicles()
        for vehicle in edge.vehicles:
            my_canvas.draw_vehicle(vehicle, edge)

        my_canvas.update_screen()

        # if(round(env.now, 1) % 5.0 == 0):
        #     if random.random() > 0.5:
        #         edge.add_vehicle(Vehicle(30, 0., 'car', 0.1))
        #     else:
        #         edge.add_vehicle(Vehicle(30, 0., 'car', 0.1))

        if(round(env.now, 1) % 10.0 == 0):
            print "time:", round(env.now, 1)
        yield env.timeout(tick)
        plt.pause(0.01)

if __name__ == '__main__':
    main()
