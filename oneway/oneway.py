import simpy
import matplotlib.pyplot as plt
from world import World


def main():
    myWorld = World(1000)

    for i in range(1):
        myWorld.add_car(2, i * 10)
    myWorld.add_car(0, 1000)

    env = simpy.Environment()
    env.process(simulate(env, myWorld, 1))
    env.run(until=1000)
    plt.show()
    

def simulate(env, world, tick):
    while True:
        world.plot_cars()
        print("time:", env.now)
        yield env.timeout(tick)


if __name__ == '__main__':
    main()
