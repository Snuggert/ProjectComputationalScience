import simpy
import random
import matplotlib.pyplot as plt
from edge import Edge


def main():
    myEdge = Edge(1000)

    myEdge.add_vehicle(0., 100., 1)
    for i in range(9, -1, -1):
        myEdge.add_vehicle(random.randint(0, 10), i * 10., 1)

    env = simpy.Environment()
    env.process(simulate(env, myEdge, 1))
    env.run(until=100)
    plt.show()


def simulate(env, edge, tick):
    while True:
        edge.move_vehicles(tick)
        edge.plot_vehicles()
        #p = 0.4
        #if random.random() < p:
        #    edge.add_vehicle(40, 0., 0)
        print("time:", env.now)
        yield env.timeout(tick)


if __name__ == '__main__':
    main()
