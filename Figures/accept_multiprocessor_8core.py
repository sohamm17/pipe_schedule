import numpy as np
import math
import matplotlib.pyplot as plt
import sys

def main():

    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '-', '--', '--']
    colors = ['#ff8080', "#00cccc", '#ff9900', 'g', 'k', 'm', 'r']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']

    # Data format
    #<first line> number of tasks per Pipeline
    #<second lines> - without opti
    #<third line> - with opo only
    #<fourth line> - with mig only
    #<fourth line> - with both

    tasks = []
    total_tasks = []
    without_opti = []
    with_mig = []
    with_opo = []
    with_both = []
    with open("accept_multiprocessor_8core.csv") as f:
        tasks = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
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
    plt.xlim(2, 10)

    ax = fig.add_subplot(111)
    plt.ylim(55, 86)

    plt.xlabel("Pipeline Length", fontsize=20)
    plt.ylabel("# of Accepted Pipelines", fontsize=20)

    bar_width = 0.4
    ypos = []
    labels = ["WFD", "+RPO only", "+mig only", "+both"]
    x = 1

    xticks = [3, 6, 9]
    # plt.xticks(xticks)
    ax.set_xticks(xticks)
    ax.set_xticklabels(["3", "5", "10"])

    i = 0
    plt.bar([x - bar_width* 1.5  for x in xticks], without_opti, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=1, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x - bar_width/2  for x in xticks], with_opo, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.8, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x + bar_width/1.5 - 0.03  for x in xticks], with_mig, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.6, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x + bar_width*1.5 + 0.08  for x in xticks], with_both, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tick_params(axis='both', which='minor', labelsize=16)

    legend = ax.legend(loc='lower left', bbox_to_anchor=(-0.01, 0.51), prop={'size': 20}, handlelength=3.0)
    legend.get_frame().set_alpha(0.5)
    plt.grid(axis='y')
    plt.tight_layout(pad=0)
    # plt.show()
    plt.savefig("accept_multiprocessor_8core.pdf")


if __name__ == "__main__":
    main()
