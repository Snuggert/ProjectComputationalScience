from edge import Edge
import random
import matplotlib.pyplot as plt
from vehicle import Vehicle

loc = [[0, 0], [900, 1200]]
tick = 0.1
init_speed = 40
init_pos = 0.
veh_type = "car"
prob = 0.01

ci = []
cb = []

myEdge = Edge(loc, 40, tick)
myEdge.add_vehicle(Vehicle(0, 1500, 'broken', tick))

t_last = 0
t0 = 0

N = 300
last_stopped = 0
last_fast = 1
braking = False
start_writing = False

for t in range(N):
    print "\nt = %d\n" % t
    if random.random() < prob:
        myEdge.add_vehicle(Vehicle(init_speed, init_pos, veh_type, tick))

    n = len(myEdge.vehicles) 

    if braking:
        print "er wordt geremd door auto %d" % last_fast
        last_fast += 1
        braking = False
        if n > last_fast and start_writing:
            ci.append((t * tick, 1500 - myEdge.vehicles[last_fast].location))

    if n > last_fast:
        fast_car = myEdge.vehicles[last_fast]
        a = fast_car.speed[1] - fast_car.speed[0]
        if a < -2:
            braking = True


    if n > last_stopped + 1:
        next_car = myEdge.vehicles[last_stopped + 1]
        if abs(next_car.speed[0]) < 0.01:
            if last_stopped == 0:
                t0 = t * tick
                start_writing = True

            last_stopped += 1
            print "auto %d is gestopt" % last_stopped
            cb.append((t * tick, 1500 - next_car.location))


    myEdge.move_vehicles()
    myEdge.plot_vehicles()


for i in cb:
    print i

x2, y = zip(*cb)
n = len(x2)
x = []
for t in x2:
    x.append(t - t0)
plt.plot(x, y, "b-*")

for i in ci:
    print i

x2, y = zip(*ci)
n = len(x2)
x = []
for t in x2:
    x.append(t - t0)
plt.plot(x, y, "r-*")

plt.xlabel("time in seconds")
plt.ylabel("distance in meters")
plt.title("c_i and c_b")

plt.show()

ci_start, ci_end = ci[0], ci[-1]
ci_approx = (ci_end[1] - ci_start[1]) / (ci_end[0] - ci_start[0])

cb_start, cb_end = cb[0], cb[-1]
cb_approx = (cb_end[1] - cb_start[1]) / (cb_end[0] - cb_start[0])
print "ci is ongeveer %.4f \ncb is ongeveer %.4f" % (ci_approx, cb_approx)