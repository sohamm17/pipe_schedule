import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import sys
import pickle

def get_pdf(tot_count):
    return tot_count / float(sum(tot_count))

def get_cdf(pdf):
    return np.cumsum(pdf)

def main():

    tasks = [3]
    wcets_tasks = []
    opt_linux = []
    driveos = []
    markers = ["s", "D", "o", "*", "v", "^"]
    linestyles = ['-', '--', ':', '--', '-', '--']
    colors = ['r', '#ff9900', 'b', "#00cccc", 'r', 'k', 'm', '#ff8080']
    patterns = ['o', 'x', '\\', '+', '.', 'O', '-']

    for t in tasks:
        wcet = []
        with open("watersdata_" + str(t), "rb") as setfile:
            wcet = pickle.load(setfile)
            wcet = [float(task[0] / 1000) for taskset in wcet for task in taskset]
            # print (wcet)
            # opt_linux.append(vals[1])
            # driveos.append(vals[2])
        wcets_tasks.append(wcet)

    # we start the range by subtracting 0.2 to take the very low delay values
    # that are achieved by driveos
    # count_opt, bins_opt = np.histogram(opt_linux, bins = 100, range=(min(driveos) - 0.2, max(wcet_3)))
    # count_driveos, bins_driveos = np.histogram(driveos, bins = 100, range=(min(driveos) - 0.2, max(wcet_3)))
    # print (count_vanilla, count_opt, count_driveos)
    # print (bins_vanilla, bins_opt, bins_driveos)
    # print (get_cdf(get_pdf(count_driveos)), get_cdf(get_pdf(count_opt)), get_cdf(get_pdf(count_vanilla)))

    fig = plt.figure(num=None, figsize=(6, 4.5), dpi=80, edgecolor='k')
    # plt.xlim(1.6, 100)
    ax = fig.add_subplot(111)
    # ax.set_xscale('log')
    # plt.ylim(0, 1.05)
    plt.xlabel("Task Budget (us)", fontsize=18)
    plt.ylabel("CDF", fontsize=18)
    # xticks = [0, 5, 10, 15, 20]
    # plt.xticks(xticks)
    # ax.plot(bins_driveos[1:], get_cdf(get_pdf(count_driveos)), color=colors[2], linestyle=linestyles[2], label="DriveOS", linewidth=3.9, alpha=1)
    #
    # ax.plot(bins_opt[1:], get_cdf(get_pdf(count_opt)), color=colors[1], linestyle=linestyles[1], label="Optimized Linux", linewidth=3.9, alpha=0.9)

    i = 0
    for t in tasks:
        count_vanilla, bins_vanilla = np.histogram(wcets_tasks[i], bins = 100, range=(min(wcets_tasks[i]), max(wcets_tasks[i])))
        ax.plot(bins_vanilla[1:], get_cdf(get_pdf(count_vanilla)), color=colors[i], linestyle=linestyles[i], linewidth=3.9, alpha=0.6)
        i += 1

    # ax.annotate("Log Scale in X-axis", xy=(12, 0.22), xytext=(12, 0.22),
    # textcoords='offset points', fontsize=14)

    # plt.axvline(x=10, color='r', linewidth=2, linestyle='--') #practical
    # plt.axvline(x=11, color='g', linewidth=2) #theoretical

    plt.tick_params(axis='both', which='major', labelsize=14)
    ax.get_xaxis().set_tick_params(which='minor', size=0)
    ax.get_xaxis().set_tick_params(which='minor', width=0)
    # we start the x tickers from bins_driveos[1] because that's the first
    # bin's edge of driveos. And driveos has the minimum value.
    # ax.set_xticks([bins_driveos[1], 3, 6, 10, 20, 40, 80])
    # ax.get_xaxis().set_major_formatter(tkr.ScalarFormatter())

    # legend = ax.legend(loc='upper left', bbox_to_anchor=(0.455, 0.62), prop={'size': 18}, handlelength=1.6, borderpad=0.1, handletextpad=0.5, ncol = 2)
    # legend.get_frame().set_alpha(0.5)
    plt.grid()
    plt.tight_layout(pad=0.15)
    #plt.show()
    plt.savefig("waters_wcet_cdf.pdf", bbox_inches='tight')


if __name__ == "__main__":
    main()
