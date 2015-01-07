import simpy
import random
import pygame
import matplotlib.pyplot as plt
from edge import Edge

white = (255, 255, 255)


def main():
    # set up pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    # set up the window
    modes = pygame.display.list_modes(32)
    if not modes:
        return
    else:
        screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 32)

    myEdge = Edge([[0, 100], [1000, 100]])
    myEdge.add_vehicle(0., 100., 1)
    for i in range(9, -1, -1):
        draw_vehicle(i * 10.0, myEdge, screen)
        myEdge.add_vehicle(random.randint(0, 10), i * 10., 1)

    env = simpy.Environment()
    env.process(simulate(env, myEdge, 1, screen))
    env.run(until=100)
    plt.show()


def simulate(env, edge, tick, screen):
    while True:
        screen.fill((0, 0, 0))
        edge.move_vehicles(tick)
        for vehicle in edge.vehicles:
            draw_vehicle(vehicle.location, edge, screen)
        #p = 0.4
        #if random.random() < p:
        #    edge.add_vehicle(40, 0., 0)
        print("time:", env.now)
        yield env.timeout(tick)
        if(len(edge.vehicles) == 0):
            break
        plt.pause(0.1)


def draw_vehicle(vehicle_location, edge, screen):
    ratio = vehicle_location / edge.edgesize

    pygame.draw.rect(screen, white, (int((edge.locations[1][0] -
                                          edge.locations[0][0]) * ratio
                                         + edge.locations[0][0]),
                                     int((edge.locations[1][1] -
                                          edge.locations[0][1]) * ratio
                                         + edge.locations[0][1]), 5, 5), 0)
    pygame.display.update()


if __name__ == '__main__':
    main()
