import pygame
import sys
import simpy
import random

import matplotlib.pyplot as plt
from edge import Edge
from vehicle import Vehicle
from canvas import Canvas
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def main():
    tick = 0.1
    myCanvas = Canvas()
    myEdge = Edge([[0, 100], [500, 100]], 30, tick)

    myEdge.add_vehicle(Vehicle(0., 400., 'broken', tick))
    for i in range(9, -1, -1):
        new_vehicle = Vehicle(random.randint(0, 10), i * 20., 'car', tick)
        myEdge.add_vehicle(new_vehicle)

    env = simpy.Environment()
    env.process(simulate(env, myEdge, 0.1, myCanvas))
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
        p = 0.02
        if random.random() < p:
            edge.add_vehicle(Vehicle(10, 0., 'car', 0.1))

        if(round(env.now, 1) % 10.0 == 0):
            print "time:", round(env.now, 1)
        yield env.timeout(tick)
        plt.pause(0.01)

if __name__ == '__main__':
    main()
