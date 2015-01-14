import random
import matplotlib.pyplot as plt

mu, sigma, theta = 0.180, 0.010, 0.012

N = 100000
rt = []

for i in range(N):
	x = random.gauss(mu, sigma)
	y = random.gammavariate(1, theta)
	z = x + y
	rt.append(z)

print sum(rt) / float(len(rt))
plt.hist(rt, 100)
plt.show()