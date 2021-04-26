import numpy as np
import math
import matplotlib.pyplot as plt
import sys

def main():

    seventy = []
    seventy_five = []
    eighty_five = []
    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '--', '-', '--']
    colors = ['#ff8080', '#ff9900', "#00cccc", 'r', 'k', 'm', 'g']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']

    with open("starting_alpha.csv") as f:
        seventy = [float(x) for x in f.readline().strip().rstrip('\n').split(",")]
        seventy_five = [float(x) for x in f.readline().strip().rstrip('\n').split(",")]
        eighty_five = [float(x) for x in f.readline().strip().rstrip('\n').split(",")]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(1.25, 3.2)
    ax = fig.add_subplot(111)
    plt.ylim(70, 560)
    plt.xlabel("Starting Alpha", fontsize=14)
    plt.ylabel("# of Unschedulable Tasks", fontsize=14)
    xticks = [1.3, 1.5, 2, 2.5, 3]
    plt.xticks(xticks)

    ax.plot(xticks, eighty_five, color=colors[2], linestyle=linestyles[2], marker=markers[2], label="85%", linewidth=3.7, markersize=6)

    ax.plot(xticks, seventy_five, color=colors[6], linestyle=linestyles[0], marker=markers[0], label="75%", linewidth=3.7, markersize=6)

    ax.plot(xticks, seventy, color=colors[1], linestyle=linestyles[1], marker=markers[1], label="70%", linewidth=3.7, markersize=6)

    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.tick_params(axis='both', which='minor', labelsize=10)

    ax.legend(loc='upper left', bbox_to_anchor=(0.25, 1.02), prop={'size': 14})
    plt.grid()
    plt.tight_layout()
    # plt.show()
    plt.savefig("starting_alpha.pdf")


if __name__ == "__main__":
    main()
