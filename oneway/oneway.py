import simpy
import matplotlib.pyplot as plt
from world import World


def main():
    myWorld = World(1000)

    myWorld.add_car(2., 0., 2.)
    for i in range(1):
        myWorld.add_car(3., 0., i * 10.)

    env = simpy.Environment()
    env.process(simulate(env, myWorld, 1))
    env.run(until=3)
    plt.show()
    

def simulate(env, world, tick):
    while True:
        world.move_cars(tick)
        print("time:", env.now)
        yield env.timeout(tick)


if __name__ == '__main__':
    main()
