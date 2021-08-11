import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random as rd


style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


xs = [0,1,2,3,4,5,6,7,8,9]
ys=[3,5,2,6,2,6,3,6,9,2]
count = 11

def animate(i):
    # graph_data = open('example.txt','r').read()
    # print("animate")
    # lines = graph_data.split('\n')
    # xs = []
    # ys = []
    # for line in lines:
    #     if len(line) > 1:
    #         x, y = line.split(',')
    #         xs.append(float(x))
    #         ys.append(float(y))

    xs.append(count + i)
    ys.append(count + i)


    # for i in range(20):
    #     xs.append(i)
    #     ys.append(i)

    ax1.clear()
    ax1.plot(xs, ys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()