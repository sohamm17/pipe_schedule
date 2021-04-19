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
    patterns = ['o', 'x', '\\', '-', '.', 'O', '+']

    data = []
    x_axis = []
    with open("stages.csv") as f:
        for line in f:
            vals = line.strip("").rstrip('\n').split(" ")
            x_axis.append(int(float(vals[0])*100))
            data.append([float(vals[1]), float(vals[2]), float(vals[3]), float(vals[4])])

    fig = plt.figure()
    plt.xlim(0.75, 5.1)
    ax = fig.add_subplot(111)
    plt.ylim(0, 1800)
    plt.ylabel("Number of tasks", fontsize=18)
    plt.xlabel("Initial Utilization (%)", fontsize=18)

    bar_width = 0.30
    ypos = []
    labels = ("First Stage", "Second Stage", "Third Stage", "Unschedulable")
    x = 1

    for c in range(0, len(x_axis)):
      ypos.append(1 + bar_width * x)
      x += 2

    data = np.array(data)
    for i in range (0, 4):
        sums = []
        for c in range(0, len(x_axis)):
          if i > 0:
            sums.append(np.sum(data[c: c + 1, 0: i]))
          else:
            sums = None
            break
        print (data[:, i])
        plt.bar(ypos, data[:, i], bar_width, color=colors[i], hatch=patterns[i],
        align='center', alpha=0.5, label=labels[i], edgecolor='k', bottom=sums)


    plt.xticks(ypos, x_axis)
    # ax.get_yaxis().set_major_formatter(tkr.ScalarFormatter())
    plt.tight_layout()

    #ax.set_xticklabels([])
    plt.tick_params(axis='both', which='major', labelsize=16)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)
    #plt.tick_params(axis='both', which='minor', labelsize=18)

    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 1.02), prop={'size': 18})
    plt.tight_layout()
    plt.savefig("stages.png", bbox_inches='tight')
    #plt.grid()
    # plt.show()



if __name__ == "__main__":
    main()
