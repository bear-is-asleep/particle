import pylab as plt
import numpy as np

X = np.linspace(0,2,1000)
Y = X**2 + np.random.random(X.shape)

plt.ion()
graph = plt.plot(X,Y)[0]
sc = plt.scatter(Y,X)

while True:
    sc.remove()
    Y = X**2 + np.random.random(X.shape)
    graph.set_ydata(Y)
    sc=plt.scatter(Y,X)
    plt.draw()
    plt.pause(0.02)