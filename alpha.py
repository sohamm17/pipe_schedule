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
    patterns = ['-', 'x', '\\', 'o', '.', 'O', '+']

    data = []
    x_axis = []
    alpha = []
    utils = []
    with open("alpha.csv") as f:
        for line in f:
            vals = line.strip('').rstrip('\n').split(" ")
            if len(vals) == 1 and vals[0] != "":
                x_axis.append(float(vals[0]))
            elif len(vals) > 1:
                utils.append(int(float(vals[0])*100))
                data.append([int(vals[1]), int(vals[2]), int(vals[3])])

    print (x_axis)
    print (data)

    fig = plt.figure()
    plt.xlim(0.75, 18)
    ax = fig.add_subplot(111)
    plt.ylim(0, 1800)
    plt.ylabel("# of tasks", fontsize=18)
    plt.xlabel("alpha", fontsize=18)

    bar_width = 0.30
    ypos = []
    labels = ("First Stage", "Second Stage", "Third Stage")
    x = 1

    yticks = []

    for c in range(0, len(utils)):
      ypos.append(1 + bar_width * x)
      if (c + 2) % 3 == 0 and c!= 0:
          yticks.append((1 + bar_width * x))
      x += 2
      if (c + 1) % 3 == 0 and c != 0:
          x += 2

    data = np.array(data)
    for i in range (0, 3):
        sums = []
        for c in range(0, len(utils)):
          if i > 0:
            sums.append(np.sum(data[c: c + 1, 0: i]))
          else:
            sums = None
            break

        plt.bar(ypos, data[:, i], bar_width, color=colors[i], hatch=patterns[i],
        align='center', alpha=0.5, label=labels[i], edgecolor='k', bottom=sums)


    plt.xticks(yticks, x_axis)
    plt.tight_layout()

    #ax.set_xticklabels([])
    plt.tick_params(axis='both', which='major', labelsize=16)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)
    #plt.tick_params(axis='both', which='minor', labelsize=18)
    #
    ax.annotate("0.65", xy=(1.05, 130), xytext=(1.05, 130),
    textcoords='offset points', fontsize=12)

    ax.annotate("0.75", xy=(1.60, 75), xytext=(1.60, 75),
    textcoords='offset points', fontsize=12)

    ax.annotate("0.85", xy=(2.2, 30), xytext=(2.2, 30),
    textcoords='offset points', fontsize=12)

    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 1.02), prop={'size': 18})
    plt.tight_layout()
    plt.savefig("alpha.pdf", bbox_inches='tight')
    # plt.grid()
    # plt.show()



if __name__ == "__main__":
    main()
