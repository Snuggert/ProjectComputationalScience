import simpy
from world import World


def main():
    myWorld = World(10000)

    for i in range(10):
        myWorld.add_car(2, i * 10)

    env = simpy.Environment()
    env.process(simulate(env, myWorld, 1))
    env.run(until=1000)
    

def simulate(env, world, tick):
    while True:
        print("time:", env.now)
        yield env.timeout(tick)


if __name__ == '__main__':
    main()
