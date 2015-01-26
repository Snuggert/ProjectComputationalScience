import random
import matplotlib.pyplot as plt

mu, sigma, theta = 0, 0.4, 1.

N = 100000
X = []

for i in range(N):
	X1 = random.gauss(mu, sigma)
	X2 = random.gammavariate(1, theta)
	X.append((X1 + X2) * 3.6)

mean = sum(X) / float(len(X))
print "E(x) = %.4f" % mean
plt.title("Distribution of individual speed deviation")
plt.xlabel("km/h")
plt.hist(X, 100)
plt.show()