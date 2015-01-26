from edge import Edge
from vehicle import Vehicle
import random
import matplotlib.pyplot as plt

locations = [[0, 0],[4800, 6400]]
matrix = True

# define function max_speed
if matrix:
	def max_speed(loc):
		if 4000 <= loc < 7000:
			return 70 / 3.6
		else:
			return 120 / 3.6
else:
	def max_speed(loc):
		return 120 / 3.6

x_start_wall = 6000
x_stop_wall = 7000

tick = 0.1
num_lanes = 3
prob = 0.10

edges = []
for i in range(num_lanes):
	edges.append(Edge(locations, max_speed, tick))
	edges[i].nr = i

	if i > 0:
		edges[i].add_neighbor(edges[i - 1], False)
		edges[i - 1].add_neighbor(edges[i], True)

plot_range = 4500, 6100

init_loc = -1000
init_speed = max_speed(init_loc)

for i in range(x_start_wall, x_stop_wall, 10):
	broken_veh = Vehicle(0, i, "broken", tick)
	broken_veh.type = "broken"
	edges[-1].add_vehicle(broken_veh)

edges[-1].add_wall(x_start_wall, x_stop_wall)

N = 5000
new = False
for t in range(N):
	if t % 10 == 0 and not new and t < 2000:
		lane = (t / 10) % num_lanes
		new = True
		new_car = Vehicle(init_speed, init_loc, "car", tick)
		new_car.type = "car"
		edges[lane].add_vehicle(new_car)
	else:
		new = False

	plot = False
	break
	for edge in edges:
		edge.change_lanes()
		edge.move_vehicles()
		if not plot:
			for veh in edge.vehicles:
				if (plot_range[0] < veh.location < plot_range[1] 
					and veh.type != "broken"):
					plot = True
					break

	if t % 5 == 0 and plot:
		edges[0].plot_vehicles(plot_range[0], plot_range[1])
