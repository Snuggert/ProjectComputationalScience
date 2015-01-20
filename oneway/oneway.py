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
    return 30


def main():
    tick = 0.1
    myCanvas = Canvas()
    myEdge = Edge([[0, 100], [500, 100]], max_speed, tick)
    myCanvas.max_edge = myEdge.edgesize

    # myEdge.add_vehicle(Vehicle(0., 200., 'broken', tick))
    # for i in range(9, 2, -1):
    #     new_vehicle = Vehicle(random.randint(0, 10), i * 20., 'car', tick)
    #     myEdge.add_vehicle(new_vehicle)

    env = simpy.Environment()
    env.process(simulate(env, myEdge, tick, myCanvas))
    env.run(until=500)
    plt.show()


def simulate(env, edge, tick, myCanvas):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        myCanvas.clear_screen((10, 10, 12))
        myCanvas.draw_edge(edge)

        edge.move_vehicles()
        for vehicle in edge.vehicles:
            myCanvas.draw_vehicle(vehicle, edge)

        myCanvas.update_screen()

        if(round(env.now, 1) % 1.5 == 0):
            # if random.random() > 0.5:
            #     edge.add_vehicle(Vehicle(30, 0., 'car', 0.1))
            # else:
            edge.add_vehicle(Vehicle(30, 0., 'car', 0.1))

        if(round(env.now, 1) % 10.0 == 0):
            print "time:", round(env.now, 1)
        yield env.timeout(tick)
        plt.pause(0.01)

if __name__ == '__main__':
    main()
