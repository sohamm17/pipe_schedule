import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import matplotlib.ticker as tkr
import matplotlib

def main():
    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', '-', '--', '-', '--']
    # colors = ['#ffcc99', "#99cccc", '#ff9999', 'r', 'k', 'm']
    colors = ['#ff8080', '#ff9900', "#00cccc", 'r', 'k', 'm', 'g']
    patterns = ['\\', 'x', '|', 'o', '.', 'O', '+']

    distributed = []
    concentrated = []

    with open("second_stage.csv") as f:
      distributed = [int(x) for x in f.readline().strip('').rstrip('\n').split(" ")]
      concentrated = [int(x) for x in f.readline().strip('').rstrip('\n').split(" ")]

    distributed = [float(x) / 10 for x in distributed]
    concentrated = [float(x) / 10 for x in concentrated]
    # print (distributed)

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(1.25, 2.75)
    ax = fig.add_subplot(111)
    plt.ylim(20, 45)
    plt.ylabel("# of Schedulable Tasks", fontsize=20)
    plt.xlabel("alpha", fontsize=20)

    bar_width = 0.15
    ypos = []
    labels = ["Concentrated", "Distributed"]
    x = 1

    xticks = [1.5, 2, 2.5]
    plt.xticks(xticks)

    i = 0
    plt.bar([x - bar_width/2 - 0.01  for x in xticks], distributed, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=1, label=labels[i], edgecolor='k', linewidth=2)
    i += 1
    plt.bar([x + bar_width/2 + 0.01  for x in xticks], concentrated, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.7, label=labels[i], edgecolor='k', linewidth=2)
    #
    # i = 0
    # ax.plot(xticks, distributed, color=colors[i], label=labels[i], marker=markers[i], linewidth=4.5, markersize=8)
    # i += 1
    # ax.plot(xticks, concentrated, color=colors[i], label=labels[i], marker=markers[i], linewidth=4.5, markersize=8)

    plt.tick_params(axis='both', which='major', labelsize=14)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)


    ax.legend(loc='upper left', bbox_to_anchor=(0.3, 1.02), prop={'size': 20}, handlelength=2.5)
    plt.tight_layout(pad=0.25)
    plt.grid()
    plt.savefig("second_stage.pdf", bbox_inches='tight')
    # plt.show()



if __name__ == "__main__":
    main()
