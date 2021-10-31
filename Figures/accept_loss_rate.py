import numpy as np
import math
import matplotlib.pyplot as plt
import sys

def main():

    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '-', '--', '--']
    colors = ['#ff8080', "#00cccc", '#ff9900', 'r', 'k', 'm', 'g']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']

    # Data format
    #<first line> all e2e factors
    #<second lines> total tasks
    #<third line> - loss-rate 0
    #<fourth line> - loss-rate 25
    #<fourth line> - loss-rate 50
    #<fourth line> - loss-rate 75

    e2efactors = []
    total_tasks = []
    loss_0 = []
    loss_25 = []
    loss_50 = []
    loss_75 = []
    with open("accept_loss_rate.csv") as f:
        e2efactors = [float(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        total_tasks = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        loss_0 = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        loss_25 = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        loss_50 = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]
        loss_75 = [int(x) for x in f.readline().strip().rstrip('\n').split(" ")]

    # convert to percentage based on total task
    loss_0 = [100 * float(loss_0[i]) / total_tasks[i] for i in range(len(total_tasks))]
    loss_25 = [100 * float(loss_25[i]) / total_tasks[i] for i in range(len(total_tasks))]
    loss_50 = [100 * float(loss_50[i]) / total_tasks[i] for i in range(len(total_tasks))]
    loss_75 = [100 * float(loss_75[i]) / total_tasks[i] for i in range(len(total_tasks))]

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    plt.xlim(5, 15)

    ax = fig.add_subplot(111)
    plt.ylim(0, 62)

    plt.xlabel("Transmission Factor [TF]", fontsize=24)
    plt.ylabel("Acceptance Ratio [AR] (%)", fontsize=24)

    bar_width = 0.4
    ypos = []
    labels = ["Loss Rate = 0%", "Loss Rate = 25%", "Loss Rate = 50%", "Loss Rate = 75%"]
    x = 1

    xticks = e2efactors
    plt.xticks(xticks)

    i = 0
    plt.bar([x - bar_width* 1.5  for x in xticks], loss_0, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x - bar_width/2  for x in xticks], loss_25, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x + bar_width/1.5 - 0.03  for x in xticks], loss_50, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    i += 1
    plt.bar([x + bar_width*1.5 + 0.08  for x in xticks], loss_75, bar_width, bottom=None, color=colors[i], hatch=patterns[i], align='center', alpha=0.5, label=labels[i], edgecolor='k', linewidth=2)

    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)

    ax.legend(loc='lower left', bbox_to_anchor=(0.42, 0.5), prop={'size': 24}, handlelength=3.0)
    plt.grid(axis='y')
    plt.tight_layout(pad=0)
    # plt.show()
    plt.savefig("accept_loss_rate.pdf")


if __name__ == "__main__":
    main()
