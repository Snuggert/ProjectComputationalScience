from edge import Edge
from vehicle import Vehicle
import random
import matplotlib.pyplot as plt

def make_new_vehicle(this_edge):
	veh_type = "car"
	if random.random() < p_truck:
		veh_type = "truck"
	new_veh = Vehicle(init_speed, init_location, veh_type, tick)
	
	new_veh.type = veh_type
	new_veh.id_nr = nr
	new_veh.t_begin = -1

	return new_veh

'''
Define constants
'''
# define sizes
locations = [[0, 0],[3000, 4000]]
plot_range = 0, 5000
start_wall, stop_wall = 2000, 3000

# define function max_speed
def max_speed(loc):
	return 25
		
# probabilities
p_place = 0.1
modulo = 15
p_truck = 0.1

# choices
random_placing = False
wall = False
use_plot = False

# initiation constants
init_speed = max_speed(0)
init_location = -2000

# number of iterations and tick
N = 2000
max_it =  10 * N
tick = 0.1

# _________________________________________________________


# initiate
nr = 0
num_clashed = 0
t = 0
results = {} # id_nr, time_in, time_out
collision_nr = []
finished = False

# make edges
num_lanes = 3
edges = []
for i in range(num_lanes):
	edges.append(Edge(locations, max_speed, tick))
	if i > 0:
		edges[i].add_neighbor(edges[i - 1], False)
		edges[i - 1].add_neighbor(edges[i], True)

edgesize = edges[0].edgesize

# first car
lane = random.randint(0, num_lanes - 1)
new_veh = make_new_vehicle(edges[lane])
very_first_veh = new_veh

if wall:
	# make wall
	for i in range(start_wall, stop_wall, 20):
		broken_veh = Vehicle(0, i, "broken" , tick)
		broken_veh.id_nr = -1
		edges[-1].add_vehicle(broken_veh)
		broken_veh.times = [0., -1]
	edges[-1].add_wall(start_wall, stop_wall)

'''
Run simulation
'''
while True:	
	time = t * tick
	place_new = False

	# placing a new vehicle?
	if random_placing:
		if random.random() < p_place:
			place_new = True
	else:
		if t % modulo == 0:
			place_new = True

	# stop with new vehicles if maximum iterations is reached
	if t >= N:
		place_new = False

	# place a vehicle and initiate a new one
	if place_new:
		edges[lane].add_vehicle(new_veh)
		nr += 1
		
		lane = random.randint(0, num_lanes - 1)
		new_veh = make_new_vehicle(edges[lane])

	# move all vehicles
	for edge in edges:
		edge.change_lanes()
		edge.move_vehicles()

	# iterate over every vehicle on the road
	num_vehicles = 0
	for edge in edges:
		for vehicle in edge.vehicles:

			# count collisions
			if vehicle in edge.collisions and vehicle.location > 0:
				if vehicle.id_nr not in collision_nr:
					collision_nr.append(vehicle.id_nr)
			else:
				num_vehicles += 1

			# start timer
			if vehicle.t_begin < 0 and vehicle.location >= 0.:
				vehicle.t_begin = time

			# end timer
			if (vehicle.location >= edge.edgesize and 
				vehicle.id_nr not in collision_nr):

				results[vehicle.id_nr] = time - vehicle.t_begin
				if not finished:
					t0 = time
				finished = True

	# plot if necessary
	if use_plot and t % 10 == 0:
		edges[0].plot_vehicles(plot_range[0], plot_range[1])

	# stop if all the cars have finished or crashed
	if not place_new and num_vehicles == 0:
		break 

	# increment the time parameter
	t += 1
	if t == max_it:
		for edge in edges:
			for vehicle in edge.vehicles:
				print "Snelheid: %.2f, locatie %.2f, type: %s , nr: %d" % \
				(vehicle.speed, vehicle.location, vehicle.type, 
						vehicle.id_nr)
		break


'''
Find results
'''
is_max = ""
if t == max_it:
	is_max = "(max)"
print "\nIteraties: %d %s" % (t, is_max)

mean_vel = []
time_intervals = []

for id_nr in results:
	interval = results[id_nr]
	mean_vel.append(edgesize / interval)
	time_intervals.append(interval)

if len(mean_vel) > 2:

	mean = sum(mean_vel) / len(mean_vel)
	mean_time = sum(time_intervals) / len(time_intervals)
	print "\nGemiddelde tijd: %.1f seconde" % mean_time 
	print "Totale afstand: %.1f meter" % edgesize 
	print "gemiddelde snelheid: %.4f m/s" % mean

	n_fin, n_crash = len(results), len(collision_nr)
	print "Aantal gefinished: %d, aantal stuk: %d" % (n_fin, n_crash)
	print "Kans op botsing: %.4f" % (n_crash / float(n_fin + n_crash))

	labda = n_fin / (time - t0)
	tot_cap = labda * mean_time
	tot_cap_scaled = tot_cap / edgesize * 1000.
	print "Gemiddelde capaciteit = %.2f auto's per km" % tot_cap_scaled

	title = "Average speed of vehicles on a %d-lane road" % num_lanes
	plt.hist(mean_vel, color = "red", alpha = 0.7)
	plt.xlabel("Average speed in m/s")
	plt.ylabel("Frequency")
	plt.title(title)
	plt.show()
else:
	print "Te weinig resultaten: eerste op %.2f" % very_first_veh.location
	print "Aantal begonnen: %d" % nr
	print "Aantal gecrashed: %d" % len(collision_nr)



