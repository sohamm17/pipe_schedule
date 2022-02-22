import numpy as np
import math
import matplotlib.pyplot as plt
import sys
from scipy.interpolate import splrep, splev, make_interp_spline

def get_smooth_x_y(list_x, list_y):
    bspl = splrep(list_x,list_y,s=3)
    bspl_y = splev(list_x,bspl)
    return bspl_y
    #X_Y_Spline = make_interp_spline(xticks, data[i])
    #X_ = np.linspace(xticks.min(), xticks.max(), 50)
    #Y_ = X_Y_Spline(X_)

def main():

    strect_factors = []
    data = [[], [], [], [], [], []]

    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '--', '-', '--']
    colors = ['#ff8080', '#ff9900', "#00cccc", 'r', 'blue', 'm', 'g']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']

    with open("waters_ar.csv") as f:
        strect_factors = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        total_tasks = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        for i in range(len(data)):
            data[i] = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    for i in range(len(data)):
        data[i] = [100 * float(data[i][j]) / total_tasks[j] for j in range(len(total_tasks))]

    #print (data)
    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(1.37, 1.77)
    ax = fig.add_subplot(111)
    plt.ylim(0, 103)
    plt.xlabel("Normalized LBG", fontsize=18)
    plt.ylabel("Acceptance Ratio [AR] (%)", fontsize=18)
    labels = ["3 tasks", "5 tasks", "8 tasks", "10 tasks", "12 tasks", "15 tasks"]
    xticks = strect_factors
    plt.xticks(xticks)

    for i in range(len(data)):
        xticks = np.array(xticks)
        data[i] = get_smooth_x_y(xticks, np.array(data[i]))
        # X_Y_Spline = make_interp_spline(xticks, data[i])
        # X_ = np.linspace(xticks.min(), xticks.max(), 50)
        # Y_ = X_Y_Spline(X_)
        ax.plot(xticks, data[i], color=colors[i], linestyle=linestyles[i], marker=markers[i], label=labels[i], linewidth=3.6, markersize=6)

    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=14)

    ax.legend(loc='upper left', bbox_to_anchor=(-0.03, 1.03), prop={'size': 18}, ncol=1, framealpha=0.2)
    plt.grid()
    plt.tight_layout(pad=0.15)
    # plt.show()
    plt.savefig("waters_ar.pdf")


if __name__ == "__main__":
    main()
