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
    if loc > 2000:
        return 20
    else:
        return 30


def main():
    tick = 0.1
    myCanvas = Canvas()
    myEdge = Edge([[0, 100], [500, 100]], max_speed, tick)
    myEdgeNeighbor = Edge([[0, 93], [500, 93]], max_speed, tick)
    myEdgeNeighborNeighbor = Edge([[0, 85], [500, 85]], max_speed, tick)

    myEdge.add_neighbor(myEdgeNeighbor, True)
    myEdgeNeighbor.add_neighbor(myEdge, False)
    myEdgeNeighbor.add_neighbor(myEdgeNeighborNeighbor, True)
    myEdgeNeighborNeighbor.add_neighbor(myEdgeNeighbor, False)

    # myEdge.add_vehicle(Vehicle(0., 400., 'broken', tick))
    # for i in range(20, -1, -1):
    #     new_vehicle = Vehicle(random.randint(0, 10), i * 20., 'car', tick)
    #     myEdge.add_vehicle(new_vehicle)

    env = simpy.Environment()
    env.process(simulate(env, [myEdge, myEdgeNeighbor, myEdgeNeighborNeighbor],
                         0.1, myCanvas))
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
            for vehicle in edge.to_change:
                edge.to_change.remove(vehicle)

                if(vehicle in edge.vehicles):
                    edge.vehicles.remove(vehicle)
                    direction = vehicle.change_lane.pop(0)
                    if(direction == 'inward'):
                        edge.inner_edge.add_vehicle(vehicle)
                    elif(direction == 'outward'):
                        i = edge.outer_edge.add_vehicle(vehicle)
                        edge.outer_edge.move_vehicle(vehicle, i)
                    else:
                        print "None made it here"
            edge.move_vehicles()
            for vehicle in edge.vehicles:
                myCanvas.draw_vehicle(vehicle, edge)

        myCanvas.update_screen()

        if(round(env.now, 1) % 1.0 == 0):
            edges[0].add_vehicle(Vehicle(30, 0., 'car', 0.1))
        if(round(env.now, 1) % 10.0 == 0):
            print "time:", round(env.now, 1)
        yield env.timeout(tick)
        plt.pause(0.01)

if __name__ == '__main__':
    main()
