from edge import Edge
from vehicle import Vehicle
import random
import matplotlib.pyplot as plt

locations = [[0, 0],[3000, 4000]]

def max_speed (loc):
	return 30

x_start_wall = 2000
x_stop_wall = 3000

tick = 0.1
num_lanes = 3
prob = 0.06

edges = []
for i in range(num_lanes):
	edges.append(Edge(locations, max_speed, tick))

	if i > 0:
		edges[i].add_neighbor(edges[i - 1], False)
		edges[i - 1].add_neighbor(edges[i], True)

plot_range = 0, edges[0].edgesize

init_loc = 0
init_speed = max_speed(init_loc)

for i in range(x_start_wall, x_stop_wall, 10):
	edges[-1].add_vehicle(Vehicle(0, i, "broken", tick))

edges[-1].start_wall = x_start_wall
edges[-1].stop_wall = x_stop_wall

N = 1000
new = False
for t in range(N):
	if random.random() < prob and not new:
		lane = random.randint(0, num_lanes - 1)
		new = True
		new_car = Vehicle(init_speed, init_loc, "car", tick)
		edges[lane].add_vehicle(new_car)
	else:
		new = False

	for edge in edges:
		edge.change_lanes()
		edge.move_vehicles()
	
	print "Time: %d" % t

	if t % 5 == 0:
		edges[0].plot_vehicles(plot_range[0], plot_range[1])
