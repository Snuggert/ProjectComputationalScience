from edge import Edge
from vehicle import Vehicle
import random
import matplotlib.pyplot as plt

locations = [[0, 0],[600, 800]]

def max_speed (loc):
	return 30

x_start_wall = 700
x_stop_wall = 800

tick = 0.1
num_lanes = 3
prob = 0.10

edges = []

for i in range(num_lanes):
	new_edge = Edge(locations, max_speed, tick)
	new_edge.nr = i
	edges.append(new_edge)

	if i > 0:
		edges[i].add_neighbor(edges[i - 1], False)
		edges[i - 1].add_neighbor(edges[i], True)

for i in range(num_lanes):
	if i < num_lanes - 1:
		edges[i].add_neighbor(edges[i + 1], True)
		edges[i + 1].add_neighbor(edges[i], False)

init_loc = 0
init_speed = max_speed(init_loc)

for i in range(x_start_wall, x_stop_wall, 10):
	edges[-1].add_vehicle(Vehicle(0, i, "broken", tick))
edges[-1].wall = x_start_wall

N = 1000
for t in range(N):
	if random.random() < prob and not new:
		lane = random.randint(0,2)
		new = True
		new_car = Vehicle(init_speed, init_loc, "car", tick)
		edges[lane].add_vehicle(new_car)
	else:
		new = False

	for edge in edges:
		for vehicle in edge.to_change:
			edge.to_change.remove(vehicle)

			if(vehicle in edge.vehicles):
				edge.vehicles.remove(vehicle)
				direction = vehicle.change_lane.pop(0)
				if(direction == 'inward'):
					edge.inner_edge.add_vehicle(vehicle)
				elif(direction == 'outward'):
					i = edge.outer_edge.add_vehicle(vehicle)
					edge.outer_edge.move_vehicle(vehicle, i)
				else:
					print "None made it here"
		edge.move_vehicles()
	
	print "Time: %d" % t

	if t % 5 == 0:
		edges[0].plot_vehicles()
