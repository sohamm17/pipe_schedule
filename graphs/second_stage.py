import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import matplotlib.ticker as tkr
import matplotlib


def main():
    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', '-', '--', '-', '--']
    colors = ['#ffcc99', '#ff9999', "#99cccc", 'r', 'k', 'm']
    

    distributed = []
    concentrated = []

    with open("second_stage.csv") as f:
      distributed = [int(x) for x in f.readline().strip('').rstrip('\n').split(",")]
      concentrated = [int(x) for x in f.readline().strip('').rstrip('\n').split(",")]

    print (distributed)

    fig = plt.figure()
    plt.xlim(1, 3.2)
    ax = fig.add_subplot(111)
    plt.ylim(0, 375)
    plt.ylabel("# of Unschedulable tasks", fontsize=14)
    plt.xlabel("alpha", fontsize=14)

    bar_width = 0.15
    ypos = []
    labels = ["Concentrated", "Distributed"]
    x = 1

    xticks = [1.5, 2, 2.5, 3]
    plt.xticks(xticks)

    i = 0
    plt.bar([x - bar_width/2 - 0.01  for x in xticks], distributed, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)
    i += 1
    plt.bar([x + bar_width/2 + 0.01  for x in xticks], concentrated, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    plt.tight_layout()

    plt.tick_params(axis='both', which='major', labelsize=12)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)


    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 1.02), prop={'size': 14})
    plt.tight_layout()
    plt.grid()
    plt.savefig("second_stage.pdf", bbox_inches='tight')
    # plt.show()



if __name__ == "__main__":
    main()
