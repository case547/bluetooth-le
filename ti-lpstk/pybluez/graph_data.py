import random
from collections import deque
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Time parameters, in seconds
INTERVAL = 0.5
HIST_LEN = 10

DEFAULT_Y_MAX = 100

fig, ax = plt.subplots()
x_data = np.arange(-HIST_LEN, 0, INTERVAL)
y_data = deque([None]*len(x_data), maxlen=len(x_data))
ln, = plt.plot([], [], 'gold', marker='o', ls='None')

def init():
    ax.set_xlim(-HIST_LEN, 0)
    ax.set_ylim(0, DEFAULT_Y_MAX)
    
    plt.xlabel('History')
    plt.ylabel('Value')
    
    return ln,

def update(datum):
    global y_data
    y_data.append(datum) 

    try:
        data_max = max(i for i in list(y_data) if i is not None)
    except:
        data_max = 0
    
    if data_max > DEFAULT_Y_MAX:
        ax.set_ylim(0, data_max * 1.1)
    else:
        ax.set_ylim(0, DEFAULT_Y_MAX)

    ln.set_data(x_data, list(y_data))
    return ln,

ani = FuncAnimation(fig, update, frames=[100,200,300,150,250], init_func=init, interval=INTERVAL*1000, blit=False)
plt.show()