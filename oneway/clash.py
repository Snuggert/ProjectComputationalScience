from edge import Edge
from vehicle import Vehicle


locations = [[0, 0],[150, 200]]
max_speed = 70
tick = 0.1
myEdge = Edge(locations, max_speed, tick)

car0 = Vehicle(10, 0, "broken", tick)
myEdge.add_vehicle(car0)

N = 200
for t in range(N):
	print "\nt = %.2f" % (t * tick)
	if t % 20 == 0:
		new_car = Vehicle(120, -200, "car", tick)
		myEdge.add_vehicle(new_car)
	myEdge.move_vehicles()
	k = 0
	for veh in myEdge.vehicles:
		print "car %d heeft plaats %.2f en snelheid %.2f" % (k, veh.location, \
			veh.speed[0])
		k += 1
	myEdge.plot_vehicles()