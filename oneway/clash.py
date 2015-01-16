from edge import Edge
from vehicle import Vehicle


locations = [[0, 0],[150, 200]]
max_speed = 68
tick = 0.1
myEdge = Edge(locations, max_speed, tick)

for i in range(1):
	car = Vehicle(0, 100 - i * 10, "broken", tick)
	myEdge.add_vehicle(car)

new_car = Vehicle(0, 0, "car", tick)
myEdge.add_vehicle(new_car)

N = 100
for t in range(N):
	print "\nt = %.2f" % (t * tick)
	myEdge.move_vehicles()
	k = 0
	for veh in myEdge.vehicles:
		print "car %d heeft plaats %.2f en snelheid %.2f" % (k, veh.location, \
			veh.speed[0])
		k += 1
	#myEdge.plot_vehicles()