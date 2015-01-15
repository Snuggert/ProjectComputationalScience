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
    myEdge = Edge([[0, 100], [500, 100]])
    myEdgeNeighbor = Edge([[0, 93], [500, 93]])

    myEdge.add_neighbor(myEdgeNeighbor, True)
    myEdgeNeighbor.add_neighbor(myEdge, False)

    myEdge.add_vehicle(Vehicle(0., 400., 'broken', tick))
    for i in range(9, -1, -1):
        new_vehicle = Vehicle(random.randint(0, 10), i * 20., 'car', tick)
        myEdge.add_vehicle(new_vehicle)

    env = simpy.Environment()
    env.process(simulate(env, [myEdge, myEdgeNeighbor], 0.1, myCanvas))
    env.run(until=500)
    plt.show()


def simulate(env, edges, tick, myCanvas):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        myCanvas.clear_screen((0, 0, 0))
        for edge in edges:
            myCanvas.draw_edge(edge)
            edge.move_vehicles(tick)
            for vehicle in edge.vehicles:
                myCanvas.draw_vehicle(vehicle, edge)

        myCanvas.update_screen()
        p = 0.015
        if random.random() < p:
            edges[0].add_vehicle(Vehicle(10, 0., 'car', 0.1))

        if(round(env.now, 1) % 10.0 == 0):
            print "time:", round(env.now, 1)
        yield env.timeout(tick)
        plt.pause(0.01)

if __name__ == '__main__':
    main()
