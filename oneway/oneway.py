import simpy
import random
import matplotlib.pyplot as plt
from world import World


def main():
    myWorld = World(1000)

    myWorld.add_car(0., 0., 100.)
    for i in range(9, -1 , -1):
        myWorld.add_car(random.randint(0, 10), 0., i * 10.)

    env = simpy.Environment()
    env.process(simulate(env, myWorld, 1))
    env.run(until=100)
    plt.show()


def simulate(env, world, tick):
    while True:
        world.move_cars(tick)
        world.plot_cars()
        print("time:", env.now)
        yield env.timeout(tick)


if __name__ == '__main__':
    main()
