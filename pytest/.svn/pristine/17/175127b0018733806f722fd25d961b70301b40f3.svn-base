#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt


def plot1():
    xData = np.arange(0, 10, 1)
    yData1 = xData.__pow__(2.0)
    yData2 = np.arange(15, 61, 5)
    plt.figure(num=1, figsize=(8, 6))
    plt.title('Plot 1', size=14)
    plt.xlabel('x-axis', size=14)
    plt.ylabel('y-axis', size=14)
    plt.plot(xData, yData1, color='b', linestyle='--', marker='o', label='y1 data')
    plt.plot(xData, yData2, color='r', linestyle='-', label='y2 data')
    plt.legend(loc='upper left')
    # plt.savefig('plot1.png', format='png')
    plt.show()


def plot2():
    mu = 0.0
    sigma = 2.0
    samples = np.random.normal(loc=mu, scale=sigma, size=1000)
    plt.figure(num=1, figsize=(8, 6))
    plt.title('Plot 2', size=14)
    plt.xlabel('value', size=14)
    plt.ylabel('counts', size=14)
    plt.hist(samples, bins=40, range=(-10, 10))
    plt.text(-9, 100, r'$\mu$ = 0.0, $\sigma$ = 2.0', size=16)
    # plt.savefig('images/plot2.png', format='png')
    plt.show();


def plot3():
    data = [33, 25, 20, 12, 10]
    plt.figure(num=1, figsize=(6, 6))
    plt.axes(aspect=1)
    plt.title('Plot 3', size=14)
    plt.pie(data, labels=('Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5'))
    # plt.savefig('images/plot3.png', format='png')
    plt.show()


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1 - y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny + dy, maxy + dy)


def plot4():
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    x = np.linspace(0, 1, 100)
    y1 = np.sin(10 * x)
    y2 = x ** 2 - 0.5
    ax1.plot(x, y1, "r", lw=2)
    ax2.plot(x, y2, "g", lw=2)
    align_yaxis(ax1, 0, ax2, 0)
    plt.title(u'中文抬头')
    plt.xlabel(u'X坐标')
    plt.ylabel(u'Y坐标')
    #plt.ylabel(u'Y1坐标')
    plt.show()


def main():
    plot4()


if __name__ == '__main__':
    main()
