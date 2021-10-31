import numpy as np
import math
import matplotlib.pyplot as plt
import sys
# from scipy.interpolate import splrep, splev
#
# def get_smooth_x_y(list_x, list_y):
#     bspl = splrep(list_x,list_y,s=1)
#     bspl_y = splev(list_x,bspl)
#     return bspl_y
    # X_Y_Spline = make_interp_spline(xticks, data[i])
    # X_ = np.linspace(xticks.min(), xticks.max(), 50)
    # Y_ = X_Y_Spline(X_)

def main():

    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '-', '--', '--']
    colors = ['red', "blue", '#ff9900', 'r', 'k', 'm', 'g']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']
    hatches = ['-', '|', '/', '\\', '+', 'x', 'o', 'O', '.', '*']

    #Data format in CSV file
    #<1st line> all pipe lengths
    #<2nd lines> accepted times
    #<3rd line> rejected times

    pipelengths = []
    accepted = []
    failed = []
    with open("runtime_pipe_length.csv") as f:
        pipelengths = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        accepted = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        failed = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(pipelengths[0] - 0.25, pipelengths[len(pipelengths) - 1] + 0.5)

    ax = fig.add_subplot(111)
    plt.ylim(0, 275)

    plt.xlabel("Pipeline Length", fontsize=18)
    plt.ylabel("Runtime (ms)", fontsize=18)
    plt.xticks(pipelengths)

    i = 0
    # print (failed, get_smooth_x_y(pipelengths, failed))
    ax.plot(pipelengths, accepted, color=colors[i], linestyle=linestyles[i], label="Schedulable", linewidth=3.6, marker=markers[i], markersize=14)

    i += 1
    ax.plot(pipelengths, failed, color=colors[i], label="Unschedulable", linewidth=3.6, marker=markers[i], markersize=14)

    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=14)

    legend = ax.legend(loc='lower left', bbox_to_anchor=(0.04, 0.6), prop={'size': 18}, handlelength=2.2)
    # legend.get_frame().set_alpha(0.5)
    plt.grid()
    plt.tight_layout(pad=0.11)
    plt.savefig("runtime_pipe_length.pdf")
    # plt.show()


if __name__ == "__main__":
    main()
