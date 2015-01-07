import simpy
import random
import matplotlib.pyplot as plt
from world import World


def main():
    myWorld = World(1000)

    myWorld.add_vehicle(0., 100., 1)
    for i in range(9, -1, -1):
        myWorld.add_vehicle(random.randint(0, 10), i * 10., 1)

    env = simpy.Environment()
    env.process(simulate(env, myWorld, 1))
    env.run(until=100)
    plt.show()


def simulate(env, world, tick):
    while True:
        world.move_vehicles(tick)
        world.plot_vehicles()
        #p = 0.4
        #if random.random() < p:
        #    world.add_vehicle(40, 0., 0)
        print("time:", env.now)
        yield env.timeout(tick)


if __name__ == '__main__':
    main()
