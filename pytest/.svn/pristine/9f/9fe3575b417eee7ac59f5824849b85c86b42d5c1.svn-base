# coding: utf-8
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import rand,randn,multivariate_normal


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# 为2*2的图像%20%20ax1为第一个图像#
ax.plot(np.arange(1000), randn(1000).cumsum(), 'b', label='one')
# x为np.arange(1000)，y为randn(1000).cumsum()%20如果不理解可以%20print%20randn(1000).cumsum()看看
ax.plot(np.arange(1000), randn(1000).cumsum(), 'r-', label='two')
ax.plot(randn(1000).cumsum(), 'k', label='three')
ticks = ax.set_xticks([0, 250, 500, 750, 1000])
# 设置刻度#
labels = ax.set_xticklabels(['one', 'two', 'three', 'four', 'five'], rotation=30, fontsize='small')
# 设置刻度标签
ax.legend(loc='best')
ax.set_title('My plot')
ax.set_xlabel('stages')
ax.text(416, 22, 'this is annotation', family='monospace', fontsize=20)
# 在图像上添加注释plt.savefig("case4.png", dpi=100)
plt.show()
