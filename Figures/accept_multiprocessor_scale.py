import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import sys

def main():

    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '-', '--', '--']
    colors = ['#ff8080', "#00cccc", '#ff9900', 'g', 'k', 'm', 'r']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']

    # Data format
    #<first line> number of cores per Pipeline
    #<second lines> - without opti
    #<third line> - with opo only
    #<fourth line> - with mig only
    #<fourth line> - with both

    cores = []
    total_tasks = []
    without_opti = []
    with_mig = []
    with_opo = []
    with_both = []
    with open("accept_multiprocessor_scale.csv") as f:
        cores = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        without_opti = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        with_opo = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        with_mig = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        with_both = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    # convert to percentage based on total task
    # without_opti = [100 * float(without_opti[i]) / total_tasks[i] for i in range(len(total_tasks))]
    # with_mig = [100 * float(with_mig[i]) / total_tasks[i] for i in range(len(total_tasks))]
    # with_opo = [100 * float(with_opo[i]) / total_tasks[i] for i in range(len(total_tasks))]
    # with_both = [100 * float(with_both[i]) / total_tasks[i] for i in range(len(total_tasks))]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(1.9, 8.2)

    ax = fig.add_subplot(111)
    plt.ylim(13, 71)

    plt.xlabel("# of Processors", fontsize=18)
    plt.ylabel("# of Accepted Pipelines", fontsize=18)

    labels = ["WFD", "+OPO only", "+mig only", "+both"]

    xticks = cores
    plt.xticks(xticks)

    i = 0
    ax.plot(xticks, without_opti, color=colors[i], label=labels[i], linewidth=3.4, linestyle=linestyles[i], marker=markers[i] , markersize=8)

    i += 1
    ax.plot(xticks, with_opo, color=colors[i], label=labels[i], linewidth=3.4, linestyle=linestyles[i], marker=markers[i] , markersize=8)

    i += 1
    ax.plot(xticks, with_mig, color=colors[i], label=labels[i], linewidth=3.4, linestyle=linestyles[i], marker=markers[i] , markersize=8)

    i += 1
    ax.plot(xticks, with_both, color=colors[i], label=labels[i], linewidth=3.4, linestyle=linestyles[i], marker=markers[i] , markersize=8)

    plt.tick_params(axis='both', which='major', labelsize=14)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)

    ax.legend(loc='lower left', bbox_to_anchor=(0.0, 0.55), prop={'size': 18}, handlelength=2.2)
    plt.grid()
    plt.tight_layout(pad=0.20)
    # plt.show()
    plt.savefig("accept_multiprocessor_scale.pdf")


if __name__ == "__main__":
    main()
