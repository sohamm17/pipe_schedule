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
    #<first line> LBGs
    #<second lines> CoPi Accepted
    #<third line> - with opo only
    #<fourth line> - with mig only
    #<fourth line> - with both

    lbg = []
    accepted_copi = []
    with_mig = []
    accepted_gekko = []
    with_both = []
    with open("lbg_time_failed.csv") as f:
        lbg = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        accepted_copi = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        accepted_gekko = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    # plt.xlim(2, 10)

    ax = fig.add_subplot(111)
    plt.ylim(100, 525)

    plt.xlabel("LBG", fontsize=20)
    plt.ylabel("Runtime (ms)", fontsize=20)

    bar_width = 0.2
    ypos = []
    labels = ["GEKKO", "CoPi"]
    x = 1

    xticks = lbg
    # plt.xticks(xticks)
    ax.set_xticks(xticks)
    # ax.set_xticklabels(lbg)

    # ax.set_yscale('log')
    i = 0
    plt.bar([x + bar_width / 2  for x in xticks], accepted_gekko, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.8, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x - bar_width / 2 for x in xticks], accepted_copi, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=1, label=labels[i], edgecolor='k', linewidth=2)

    # i += 1
    # plt.bar([x + bar_width/1.5 - 0.03  for x in xticks], with_mig, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.6, label=labels[i], edgecolor='k', linewidth=2)
    #
    # i += 1
    # plt.bar([x + bar_width*1.5 + 0.08  for x in xticks], with_both, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tick_params(axis='both', which='minor', labelsize=16)

    ax.legend(loc='lower left', bbox_to_anchor=(0.5, 0.72), prop={'size': 20}, handlelength=3.0)
    plt.grid(axis='y')
    plt.tight_layout(pad=0.13)
    # plt.show()
    plt.savefig("lbg_time_failed.pdf")


if __name__ == "__main__":
    main()
