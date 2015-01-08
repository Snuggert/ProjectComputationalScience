import pygame
import sys
import simpy
import random
import matplotlib.pyplot as plt
from edge import Edge
from canvas import Canvas
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def main():
    myCanvas = Canvas()
    myEdge = Edge([[0, 100], [500, 100]])
    myEdge.add_vehicle(0., 100., 1)
    for i in range(9, -1, -1):
        myEdge.add_vehicle(random.randint(0, 10), i * 10., 1)

    env = simpy.Environment()
    env.process(simulate(env, myEdge, 0.1, myCanvas))
    env.run(until=100)
    plt.show()


def simulate(env, edge, tick, myCanvas):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        myCanvas.clear_screen((0, 0, 0))
        myCanvas.draw_edge(edge)
        edge.move_vehicles(tick)
        for vehicle in edge.vehicles:
            myCanvas.draw_vehicle(vehicle, edge)

        myCanvas.update_screen()
        #p = 0.4
        #if random.random() < p:
        #    edge.add_vehicle(40, 0., 0)
        print("time:", env.now)
        yield env.timeout(tick)
        if(len(edge.vehicles) == 0):
            break
        plt.pause(0.05)


if __name__ == '__main__':
    main()
