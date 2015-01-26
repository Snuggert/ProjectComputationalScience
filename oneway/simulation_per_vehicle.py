from edge import Edge
from vehicle import Vehicle
import random
import math
import matplotlib.pyplot as plt

def make_new_vehicle(this_edge):
	veh_type = "car"
	if random.random() < p_truck:
		veh_type = "truck"
	new_veh = Vehicle(init_speed, init_location, veh_type, tick)
	new_veh.type = veh_type

	if veh_type == "car":
		new_veh.car = True
	else:
		new_veh.car = False

	new_veh.id_nr = nr
	new_veh.t_begin = -1

	return new_veh

class Info:
	def __init__(self):
		return

'''
Define constants
'''
# define sizes
locations = [[0, 0],[4800, 6400]]
start_wall, stop_wall = 6000, 7000
num_lanes = 2
		
# probabilities
labda_place = 1/8. # per second per lane
p_truck = 0.10

# choices
wall = True
write = True
matrix = True # voeg matrixborden toe
histogram = True
use_plot = False

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

# initiation constants
init_speed = max_speed(0)
init_location = -1000
count_in = 0

# number of iterations and tick
N = 10000
max_it = 10 * N
tick = 0.05
p_place = labda_place * tick * num_lanes

# _________________________________________________________


# initiate
nr = 0
num_clashed = 0
t = 0
results = {} # id_nr -> Info
collision_nr = []
started = False
just_placed = False
find_t_react = 0

# make edges
edges = []
for i in range(num_lanes):
	this_edge = Edge(locations, max_speed, tick)
	this_edge.edge_nr = i
	edges.append(this_edge)
	if i > 0:
		edges[i].add_neighbor(edges[i - 1], False)
		edges[i - 1].add_neighbor(edges[i], True)

edgesize = edges[0].edgesize

if wall:
	# make wall
	for i in range(start_wall, stop_wall, 20):
		broken_veh = Vehicle(0, i, "broken" , tick)
		broken_veh.type = "broken"
		broken_veh.id_nr = -1
		broken_veh.t_begin = 0.
		edges[-1].add_vehicle(broken_veh)
	edges[-1].add_wall(start_wall, stop_wall)

'''
Run simulation
'''
while True:	
	time = t * tick
	place_new = False

	if t % 1000 == 0:
		print "Iteraties tot nu toe: %d" % t

	# placing a new vehicle?
	if random.random() < p_place * num_lanes and not just_placed:
		place_new = True

	# stop with new vehicles if maximum iterations is reached
	if t >= N:
		place_new = False
		vehs = edges[0].vehicles
		if use_plot:
			interval = (4800, 6100)
			plot = False
			for veh in vehs:
				if (interval[0] < veh.location < interval[1] 
					and veh.id_nr != -1 
					and	veh.id_nr not in collision_nr):
					plot = True
					break

			if t % 5 == 0 and plot:
				edges[0].plot_vehicles(interval[0], interval[1])

	# place a vehicle and initiate a new one
	if place_new:
		lane = random.randint(0, num_lanes - 1)
		new_veh = make_new_vehicle(edges[lane])
		edges[lane].add_vehicle(new_veh)
		nr += 1
		just_placed = True
	else:
		just_placed = False

	# move all vehicles
	for edge in edges:
		edge.change_lanes()
		edge.move_vehicles()

	continue_simulation = False
	number_of_veh = 0

	# iterate over every vehicle on the road
	for edge in edges:
		for vehicle in edge.vehicles:
			# count collisions
			this_nr = vehicle.id_nr
			if vehicle in edge.collisions and vehicle.location > 0:
				if vehicle.id_nr not in collision_nr and this_nr != -1:
					collision_nr.append(vehicle.id_nr)

			# is the simulation finished?
			if this_nr not in collision_nr and this_nr != -1:
				continue_simulation = True
				number_of_veh += 1
			else:
				vehicle.wants_to_go_right = False

			# start timer
			if vehicle.t_begin < 0 and vehicle.location >= 0.:
				vehicle.t_begin = time
				if not started:
					t0 = time
					print "The timer has started has started on t = %.2f" % t0
				started = True
				t1 = time
				count_in += 1

			# end timer
			if (vehicle.location >= edgesize and 
				vehicle.id_nr not in collision_nr):

				new = Info()
				new.avg_speed = edgesize / (time - vehicle.t_begin) 
				new.t_react, new.car, new.automax = (vehicle.t_react, 
					vehicle.car, vehicle.auto_max)
				results[vehicle.id_nr] = new

	# stop if all the cars have finished or crashed
	if t > N and not continue_simulation:
		break 

	# increment the time parameter
	t += 1

	# maximum number of iterations reached
	if t == max_it:
		print ""
		for edge in edges:
			for vehicle in edge.vehicles:
				if vehicle.type != "broken":
					print "Snelheid: %.2f, locatie %.2f, edge: %d , wtgr: %d" % \
					(vehicle.speed, vehicle.location, edge.edge_nr, 
							vehicle.wants_to_go_right)
		break

'''
Find results
'''
print "\nEr waren %d iteraties" % t
n_fin, n_crash = len(results), len(collision_nr)
print "Er zijn %d gefinished en %d gecrashed" % (n_fin, n_crash)

if started and t1 > t0:
	rate_in = count_in / (t1 - t0) / num_lanes
	print "stroom in: %.2f per seconde per baan" % rate_in

if (n_fin + n_crash) > 0:
	p_crash = float(n_crash) / (n_fin + n_crash) 
	print "kans op clash: %.4f" % p_crash
	if write:
		f = open("results_per_vehicle.txt", "a")
		for id_nr in results:
			inf = results[id_nr]
			tup = (inf.avg_speed * 3.6,
				inf.t_react,
				inf.car,
				matrix,
				rate_in,
				inf.automax * 3.6,
				p_crash,
				num_lanes)
			s = ""
			for i, item in enumerate(tup):
				if i != 0:
					s += ","
				s += "%.4f" % item
				f.write(s)
				s = ""
			f.write("\n")
		f.close()

	if histogram:
		hist = []
		for id_nr in results:
			inf = results[id_nr]
			hist.append(inf.avg_speed * 3.6)

		title = "Average speed of vehicles on a %d-lane road" % num_lanes
		plt.hist(hist, color = "red", alpha = 0.7)
		plt.xlabel("Average speed in km/h")
		plt.ylabel("Frequency")
		plt.title(title)
		plt.show()





