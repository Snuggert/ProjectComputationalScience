from edge import Edge
from vehicle import Vehicle
import random
import matplotlib.pyplot as plt

def make_new_vehicle():
	veh_type = "car"
	if random.random() < p_truck:
		veh_type = "truck"
	new_veh = Vehicle(init_speed, init_location, veh_type, tick)

	new_veh.nr = nr
	results[nr] = [-1, -1]
	new_veh.out_of_edge = False

	if len(edge.vehicles) > 0:
		new_veh.before = edge.vehicles[-1]
		new_veh.min_gap = new_veh.before.length + \
			0.5 * init_speed * init_speed / new_veh.max_brake +\
			new_veh.t_react * new_veh.speed
	else:
		new_veh.before = new_veh
		new_veh.min_gap = 0

	return new_veh

'''
Define constants
'''
locations = [[0, 0],[2400, 3200]]
def max_speed(loc):
	if loc > 2000:
		return 20
	else:
		return 30
		
tick = 0.1
edge = Edge(locations, max_speed, tick)

init_speed = 30
init_location = 0
p_place = 0.1
p_truck = 0.1

results = {} # nr, time_in, time_out

N = 6000
nr = 0
num_clashed = 0

new_veh = make_new_vehicle()
very_first_veh = new_veh

'''
Run simulation
'''
for t in range(N):
	time = t * tick

	if len(edge.vehicles) > 0:
		in_front = edge.vehicles[-1]
		gap = in_front.location - init_location
		if gap > new_veh.min_gap:
			valid = True
	else:
		valid = True

	if valid and random.random() < p_place:
		edge.add_vehicle(new_veh)
		results[nr][0] = time
		nr += 1
		
		valid = False
		new_veh = make_new_vehicle()

	edge.move_vehicles()
	#edge.plot_vehicles()

	if len(edge.vehicles) > 0:
		first_veh = edge.vehicles[0]
		if first_veh.before == first_veh:
			continue

		before_veh = first_veh.before
		# test whether the car in front of it just went out of the edge
		while not before_veh.out_of_edge:
			before_veh.out_of_edge = True
			this_nr = before_veh.nr
			results[this_nr][1] = time 
			if before_veh.location < edge.edgesize:
				results[nr][1] = -1
				print "veh nr %d is kaput" % this_nr
				num_clashed += 1

			before_veh = before_veh.before

'''
Find results
'''
nrs = []
interval = []

for nr in results:
	times = results[nr]
	if times[1] > 0:
		nrs.append(nr)
		interval.append(times[1] - times[0])

if len(nrs) > 1:
	xmax = max(nrs)
	ymax = max(interval) * 1.80

	mean = sum(interval) / len(interval)
	mean2 = sum(interval[5:]) / len(interval[5:])
	print "\ngemiddelde tijd: %.1f seconde" % mean 
	print "Totale afstand: %.1f meter" % edge.edgesize 
	print "gemiddelde snelheid: %.4f m/s" % (edge.edgesize / mean)
	print "aangepast gemiddelde snelheid: %.4f m/s" % \
		(edge.edgesize / mean2) 

	print "Totaal aantal auto's: %d" % nr
	kapot = num_clashed + len(edge.collisions)
	print "Aantal auto's kapot: %d (%.2f procent)" % \
		(kapot, (kapot * 100.0) / nr)

	plt.plot(nrs, interval, "r-*")
	plt.axis([0, xmax, 0, ymax])
	plt.show()
else:
	print "Te weinig resultaten"



