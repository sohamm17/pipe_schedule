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

    #Data format in CSV file
    #<1st line> all loss rates
    #<2nd lines> total tasks
    #<3rd line> accepted by CoPi
    #<4th line> accepted by GEKKO
    #<5th line> accepted by GEKKO + Budget Adjustment Constraint (BAC)

    lossrates = []
    total_tasks = []
    copi = []
    gekko = []
    gekko_bac = []
    with open("accept_models_lr.csv") as f:
        lossrates = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        total_tasks = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        copi = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        gekko = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        gekko_bac = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    # convert to percentage based on total task
    copi = [100 * float(copi[i]) / total_tasks[i] for i in range(len(total_tasks))]
    gekko = [100 * float(gekko[i]) / total_tasks[i] for i in range(len(total_tasks))]
    gekko_bac = [100 * float(gekko_bac[i]) / total_tasks[i] for i in range(len(total_tasks))]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(lossrates[0], lossrates[len(lossrates) - 1])

    ax = fig.add_subplot(111)
    plt.ylim(0, 58)
    plt.xlim(0, 75.5)

    plt.xlabel("Loss Rate Upper Bound (%)", fontsize=18)
    plt.ylabel("Acceptance Ratio [AR] (%)", fontsize=18)
    plt.xticks(lossrates)

    i = 0
    # print (gekko, get_smooth_x_y(lossrates, gekko))
    ax.fill_between(lossrates, gekko, color=colors[i], linestyle=linestyles[i], label="GEKKO", edgecolor='#000000', linewidth=0.5)#, marker=markers[i], markersize=12)

    i += 1
    ax.fill_between(lossrates, copi, color=colors[i], label="CoPi", edgecolor='#000000', hatch=hatches[i], linewidth=0.5)#, marker=markers[i], markersize=12)
    
    i += 1
    ax.fill_between(lossrates, gekko_bac, color=colors[i], label="GEKKO (with BAC)", edgecolor='#000000', hatch=hatches[i], linewidth=0.5)#, marker=markers[i], markersize=12)

    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=14)

    legend = ax.legend(loc='lower left', bbox_to_anchor=(0.00, 0.66), prop={'size': 18}, handlelength=2.2)
    legend.get_frame().set_alpha(0.5)
    plt.grid()
    plt.tight_layout(pad=0.13)
    plt.savefig("accept_models_lr.pdf")
    # plt.show()


if __name__ == "__main__":
    main()
