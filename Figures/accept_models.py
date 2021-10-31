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
    colors = ['#ff8080', "#00cccc", '#ff9900', 'r', 'k', 'm', 'g']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']
    hatches = ['-', '|', '/', '\\', '+', 'x', 'o', 'O', '.', '*']

    # Data format
    #<first line> all e2e factors
    #<second lines> total tasks
    #<third line> accepted by CoPi
    #<fourth line> accepted by CoPi - Harmonic - not used
    #<fifth line> accepted by GEKKO
    #<sixth line> accepted by scipy (trust-constr)
    #<third line> accepted by pyomo
    e2efactors = []
    total_tasks = []
    copi = []
    copi_wo_harmonic = []
    gekko = []
    pyomo_incr = []
    pyomo = []
    with open("accept.csv") as f:
        e2efactors = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        total_tasks = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        copi = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        copi_wo_harmonic = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        gekko = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        pyomo_incr = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        pyomo = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    # convert to percentage based on total task
    copi = [100 * float(copi[i]) / total_tasks[i] for i in range(len(total_tasks))]
    copi_wo_harmonic = [100 * float(copi_wo_harmonic[i]) / total_tasks[i] for i in range(len(total_tasks))]
    gekko = [100 * float(gekko[i]) / total_tasks[i] for i in range(len(total_tasks))]
    pyomo_incr = [100 * float(pyomo_incr[i]) / total_tasks[i] for i in range(len(total_tasks))]
    pyomo = [100 * float(pyomo[i]) / total_tasks[i] for i in range(len(total_tasks))]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(e2efactors[0], e2efactors[len(e2efactors) - 1])

    ax = fig.add_subplot(111)
    plt.ylim(0, 105)

    plt.xlabel("Latecy Budget Gap [LBG]", fontsize=18)
    plt.ylabel("Acceptance Ratio [AR] (%)", fontsize=18)
    plt.xticks(e2efactors)

    # ax.plot(e2efactors, pyomo_incr, color=colors[4], linestyle=linestyles[4], marker=markers[4], label="Increasing\nperiod", linewidth=3.7, markersize=6)
    #
    # ax.plot(e2efactors, gekko, color=colors[2], linestyle=linestyles[2], marker=markers[2], label="gekko (APOPT)", linewidth=3.7, markersize=6)
    #
    # ax.plot(e2efactors, copi, color=colors[0], linestyle=linestyles[0], marker=markers[0], label="CoPi", linewidth=3.7, markersize=6)
    #
    # # ax.plot(e2efactors, copi_wo_harmonic, color=colors[1], linestyle=linestyles[1], marker=markers[1], label="CoPi-w/o RMS\nharmonic bound", linewidth=3.7, markersize=6)
    #
    # ax.plot(e2efactors, pyomo, color=colors[3], linestyle=linestyles[3], marker=markers[3], label="pyomo (IPOPT)", linewidth=3.7, markersize=6)

    i = 0
    # print (gekko, get_smooth_x_y(e2efactors, gekko))
    ax.fill_between(e2efactors, gekko, color=colors[i], linestyle=linestyles[i], label="GEKKO (APOPT)", linewidth=0.5, edgecolor='#000000')

    i += 1
    ax.fill_between(e2efactors, copi, color=colors[i], label="CoPi", edgecolor='#000000', linewidth=0.5, hatch=hatches[i])
    i += 1
    ax.fill_between(e2efactors, pyomo, color=colors[i], label="pyomo (IPOPT)", linewidth=0.5, edgecolor='#000000', hatch=hatches[i])
    i += 1
    ax.fill_between(e2efactors, pyomo_incr, color=colors[i], linestyle=linestyles[i], label="scipy (trust-constr)", linewidth=0.5, edgecolor='#000000', hatch=hatches[i])

    # ax.fill_between(e2efactors, 0, copi_wo_harmonic, color=colors[i], linestyle=linestyles[i], label="CoPi-w/o RMS\nharmonic bound", linewidth=3.7, alpha=0.5)


    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=14)

    legend = ax.legend(loc='lower left', bbox_to_anchor=(-0.02, 0.57), prop={'size': 18}, handlelength=1.5)
    legend.get_frame().set_alpha(0.5)
    plt.grid()
    plt.tight_layout(pad=0.11)
    plt.savefig("accept_models.pdf")
    # plt.show()


if __name__ == "__main__":
    main()
