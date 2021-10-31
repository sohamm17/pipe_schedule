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
    colors = ['#ff8080', "#00cccc", '#ff9900', 'r', 'k', 'm', 'g']
    patterns = ['-', 'x', '\\', 'o', '.', 'O', '+']

    decr_alpha = []
    incr_alpha = []
    stretch_factors = []

    with open("num_iterations.csv") as f:
        stretch_factors = [float(x) for x in f.readline().strip('').rstrip('\n').split(" ")]
        decr_alpha = [float(x) for x in f.readline().strip('').rstrip('\n').split(" ")]
        incr_alpha = [float(x) for x in f.readline().strip('').rstrip('\n').split(" ")]

    # print (decr_alpha)

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(1.29, 1.51)
    ax = fig.add_subplot(111)
    plt.ylim(0, 35)
    plt.ylabel("Avg. # of Iterations", fontsize=20)
    plt.xlabel("NLBG", fontsize=20)

    bar_width = 0.15
    ypos = []
    labels = ["Decr. alpha", "Incr. alpha"]
    x = 1

    xticks = stretch_factors
    plt.xticks(xticks)

    # i = 0
    # plt.bar([x - bar_width/2 - 0.01  for x in xticks], decr_alpha, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=1, label=labels[i], edgecolor='k', linewidth=2)
    #
    # i += 1
    # plt.bar([x + bar_width/2 + 0.01  for x in xticks], incr_alpha, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.7, label=labels[i], edgecolor='k', linewidth=2)

    i = 0
    ax.plot(xticks, decr_alpha, color=colors[i], label=labels[i], marker=markers[i], linewidth=4.5, markersize=12)

    i += 1
    ax.plot(xticks, incr_alpha, color=colors[i], label=labels[i], marker=markers[i], linewidth=4.5, markersize=12)

    plt.tick_params(axis='both', which='major', labelsize=14)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)


    ax.legend(loc='upper left', bbox_to_anchor=(0.01, 1.02), prop={'size': 20}, handlelength=2.5)
    plt.tight_layout(pad=0.25)
    plt.grid()
    plt.savefig("num_iterations.pdf", bbox_inches='tight')
    # plt.show()



if __name__ == "__main__":
    main()
