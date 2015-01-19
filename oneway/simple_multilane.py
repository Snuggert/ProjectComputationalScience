from edge import Edge
from vehicle import Vehicle
import random
import matplotlib.pyplot as plt

locations = [[0, 0],[300, 400]]

def max_speed (loc):
	if loc > 200:
		return 10
	return 30

tick = 0.1
num_lanes = 5

edges = []

for i in range(num_lanes):
	edges.append(Edge(locations, max_speed, tick))
	if i > 0:
		edges[i].add_neighbor(edges[i - 1], False)
		edges[i - 1].add_neighbor(edges[i], True)

for i in range(num_lanes):
	if i < num_lanes - 1:
		edges[i].add_neighbor(edges[i + 1], True)
		edges[i + 1].add_neighbor(edges[i], False)

init_loc = 0
init_speed = max_speed(init_loc)

N = 300
for t in range(N):
	if t % 10 == 0:
		new_car = Vehicle(init_speed, init_loc, "car", tick)
		edges[0].add_vehicle(new_car)

	for edge in edges:
		edge.move_vehicles()
	
	print "Time: %d" % t

	edges[0].plot_vehicles()
