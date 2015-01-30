from edge import Edge
import random
import matplotlib.pyplot as plt
from vehicle import Vehicle

loc = [[0, 0], [600, 800]]
tick = 0.1
max_speed = 20
init_speed = 21
init_pos = 0.
veh_type = "car"
loc_broken = 1000
prob = 0.01

ci = []
cb = []

myEdge = Edge(loc, max_speed, tick)
myEdge.add_vehicle(Vehicle(0, loc_broken, 'broken', tick))

t_last = 0
t0 = 0

N = 1000
last_stopped = 0
last_fast = 1
braking = False

for t in range(N):
    if t % 10 == 0:
        myEdge.add_vehicle(Vehicle(init_speed, init_pos, veh_type, tick))

    n = len(myEdge.vehicles) 

    if braking:
        braking = False
        ci.append((t * tick, loc_broken - 
            myEdge.vehicles[last_fast].location))
        if last_fast == 1:
            t0 = t * tick

        last_fast += 1

    if n > last_fast:
        fast_car = myEdge.vehicles[last_fast]
        a = fast_car.speed[1] - fast_car.speed[0]
        if a < -2.0 * fast_car.t_react:
            braking = True
            print "\n(n = %d) er wordt geremd door auto %d op plaats %.2f" % (n, \
                last_fast, myEdge.vehicles[last_fast].location)
            print "Deze remt met %.2f m/s2\n" % (a / fast_car.t_react)


    if n > last_stopped + 1:
        next_car = myEdge.vehicles[last_stopped + 1]
        if abs(next_car.speed[0]) < 0.01:

            last_stopped += 1
            print "auto %d is gestopt op plaats %.2f" % (last_stopped, \
                myEdge.vehicles[last_stopped].location)
            cb.append((t * tick, loc_broken - next_car.location))


    myEdge.move_vehicles()
    #myEdge.plot_vehicles()


if len(cb) > 0:
    x2, y = zip(*cb)
    n = len(x2)
    x = []
    for t in x2:
        x.append(t - t0)
    plt.plot(x, y, "b-*", label="c_b")

if len(ci) > 0:
    x2, y = zip(*ci)
    n = len(x2)
    x = []
    for t in x2:
        x.append(t - t0)
    plt.plot(x, y, "r-*", label="c_i")

if len(ci) > 0 or len(cb) > 0:
    plt.xlabel("time in seconds")
    plt.legend()
    plt.ylabel("distance in meters")
    plt.title("c_i and c_b")

    plt.show()

if len(ci) > 1 and len(cb) > 1:
    ci_start, ci_end = ci[0], ci[-1]
    ci_approx = (ci_end[1] - ci_start[1]) / (ci_end[0] - ci_start[0])

    cb_start, cb_end = cb[0], cb[-1]
    cb_approx = (cb_end[1] - cb_start[1]) / (cb_end[0] - cb_start[0])
    print "ci is ongeveer %.4f \ncb is ongeveer %.4f" % (ci_approx, cb_approx)
else:
    print "bepalen van ci en cb niet mogelijk" 