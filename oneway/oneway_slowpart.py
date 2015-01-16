from edge import Edge
import random
import matplotlib.pyplot as plt
from vehicle import Vehicle

def plot_vehicles(edges):
	n = len(edges)
	xmax = 0
	for i in range(n):
		xmax += edges[i].edgesize

	vehicles_xy = [[], []]
	x_start = 0
	for i in range(n):
		ed = edges[i]
		for vehicle in ed.vehicles:
			vehicles_xy[0].append(vehicle.location + x_start)
			vehicles_xy[1].append(1)
		x_start += ed.edgesize

	plt.plot(vehicles_xy[0], vehicles_xy[1], 'bs')
	plt.axis([0, xmax, 0, 2])
	plt.draw()
	plt.pause(0.0005)
	plt.clf()

loc = [[0, 0], [600, 800]]
prob = 0.2
tick = 0.1
init_speed = 20
init_pos = 0
veh_type = "car"

edges = [Edge(loc, 40, tick), Edge(loc, 8, tick), Edge(loc, 40, tick)]
n = len(edges)

t_last = 0
N = 300
for t in range(N):
	p = random.random()
	if p < prob and t_last < (t - 1):
		edges[0].add_vehicle(Vehicle(init_speed, init_pos, veh_type, tick))
		t_last = t

	for i in range(n - 1, -1, -1):
		ed = edges[i]
		ed.move_vehicles()

		if len(ed.collisions) > 0:
			for car in ed.collisions:
				print "auto stuk op x = %d op edge %d" % (car.location, i)

		if i == n - 1:
			continue

		for vehicle in ed.vehicles:
			if vehicle.location > ed.edgesize:
				new_loc = vehicle.location % ed.edgesize
				new_car = Vehicle(init_speed, new_loc, veh_type, tick)
				new_car.speed = vehicle.speed
				edges[i + 1].vehicles.append(new_car)

				ed.vehicles.remove(vehicle)

	plot_vehicles(edges)


