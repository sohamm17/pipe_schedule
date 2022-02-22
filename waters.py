'''
These experiments are with dataset generated from the parameters provided in
WATERS 2015 Bosch paper.
Kramer, Simon, Dirk Ziegenbein, and Arne Hamann. "Real World Automotive Benchmarks For Free," 6, 2015.
'''
from copi_lib import *

import numpy as np
import math
import matplotlib.pyplot as plt
import sys, os, pickle, getopt
from utility import *
from pipeline import *
import random
from timeit import default_timer as timer

# The algorithm is to get a random number for ACET
# from a minimum and maximum ACET value (Table IV)
# Then generate a random factor from a minimum
# and max random factor (Table V)
# Then multiply random ACET with random factor

# Table III, omitting angle-sync tasks
task_distr = [3, 2, 2, 25, 25, 3, 20, 1, 4]
# ns from Table IV
acet_distr = [5000, 4200, 11040, 10090, 8740, 17560, 10530, 2560, 430]
# from Table V (Column 3)
LOW_WCET_FACTOR = [1.30, 1.54, 1.13, 1.06, 1.06, 1.13, 1.02, 1.03, 1.84]
# from Table V (Column 4)
HIGH_WCET_FACTOR = [29.11, 19.04, 18.44, 30.03, 15.61, 7.76, 8.88, 4.90, 4.75]

# def gen_waters_wcet():
#     rand_acet = random.randint(LOW_ACET, HIGH_ACET)
#     rand_wcet_factor = random.randint(LOW_WCET_FACTOR, HIGH_WCET_FACTOR)
#     return (rand_acet * rand_wcet_factor)

# in total, generate nsets number of tasksets of n WATERS WCETs
def gen_waters_wcets(nsets, n):
    global task_distr, acet_distr, LOW_WCET_FACTOR, HIGH_WCET_FACTOR
    tasksets = []
    indx = list(range(len(task_distr)))
    for i in range(nsets):
        cur_choice = random.choices(indx, weights = task_distr, k = n)
        cur_taskset = []
        for j in cur_choice:
            acet = acet_distr[j]
            low_wcet = LOW_WCET_FACTOR[j]
            high_wcet = HIGH_WCET_FACTOR[j]
            cur_wcet = int(acet * random.uniform(low_wcet, high_wcet))
            # append fake periods because other functions
            # expect a (budget, period) tuple
            cur_taskset.append((cur_wcet, 0))
        tasksets.append(cur_taskset)
    # print (tasksets)
    return tasksets


def main(argv):
    Loss_Rate = 25 # In Percentage
    loss_ub = float(Loss_Rate) / 100
    accepted_num_iterations = []
    accepted_time_taken = []
    rejected_time_taken = []
    loss_ub = -1
    e2e_delay_factor = -1
    no_tasks = -1
    nlbg = 1.5

    # Taking arguments

    usage = 'Usage: python waters.py -n <no of tasks> -l <loss_rate> -x <NLBG, default is 1.5>'

    try:
        opts, args = getopt.getopt(argv, "n:l:x:")
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            loss_ub = float(arg)
            if loss_ub > 1:
                print ("loss_rate cannot be more than 1. cannot proceed.")
                sys.exit(1)
        elif opt == '-x':
            nlbg = float(arg)
        elif opt == '-n':
            no_tasks = int(arg)

    if no_tasks <= 0:
        print ("number of tasks is not given.")
        print (usage)
        sys.exit(1)

    if loss_ub == -1:
        print ("Loss Rate UB is not provided.")
        print (usage)
        sys.exit(1)

    if nlbg < 1:
        print ("NLBG should be more than 1.")
        print (usage)
        sys.exit(1)

    Loss_Rate = int(100 * loss_ub)

    e2e_delay_factor = float(no_tasks) * nlbg #LBG

    random.seed(50)
    no_tasksets = 1000

    current_sets = gen_waters_wcets(no_tasksets, no_tasks)

    first_schedl = 0
    second_schedl = 0
    third_schedl = 0

    setfile_string = "watersdata_" + str(no_tasks)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    done_tasksets = 0
    e2e_delay_sum = 0 # to keep track of average e2e delay for schedulables
    for single_set in current_sets:
        # print ("single_set: ", single_set)
        budgets = [x[0] for x in single_set]
        # budgets = [random.randint(5, 250) for x in single_set]
        print ("Initial Budgets: ", budgets)
        # periods = [x[1] for x in single_set]
        # single_set = [(budgets[i], periods[i]) for i in range(len(single_set))]

        # we calculate end_to_end delay_ub as a factor of the summation of budgets
        e2e_delay_ub = int(sum(budgets) * e2e_delay_factor)
        print ("Sum Budgets: {}, E2E_UB: {}".format(sum(budgets), e2e_delay_ub))

        start = timer()
        equal_period = e2e_delay_ub // (no_tasks + 1)

        #Step 1
        taskset = [(b, equal_period) for b in budgets]

        print ("First stage:", taskset, end_to_end_delay_durr(taskset), loss_rate_ub(taskset, budgets), get_total_util(taskset) * 100)

        if utilization_bound_test(taskset) and end_to_end_delay_durr(taskset) <= e2e_delay_ub and loss_rate_ub(taskset, budgets) <= loss_ub:
            # print (get_total_util(taskset))
            first_schedl += 1
            opt_alpha = 1
            e2e_delay_sum += end_to_end_delay_durr(taskset)
        else:
            # print ("Second Stage", taskset, get_total_util(taskset))

            #Step 2
            opt_alpha = optimize_alpha_all(single_set, budgets, equal_period, e2e_delay_ub, loss_ub, starting_alpha = 2)
            # if opt_alpha > 1:
            #     print ("max, min:", max(budgets), min(budgets))

            if opt_alpha == 2:
                second_schedl += 1
                e2e_delay_sum += end_to_end_delay_durr(taskset)
            elif opt_alpha == 3:
                third_schedl += 1
                e2e_delay_sum += end_to_end_delay_durr(taskset)

        end = timer()

        if opt_alpha > 1:
            accepted_time_taken.append((end - start))
        elif opt_alpha < 1:
            rejected_time_taken.append((end - start))

        done_tasksets += 1
        print ("{} Completed Tasksets.".format(done_tasksets))
        print ("first schedulable: {}/{}".format(first_schedl, done_tasksets))

        print ("second schedulable: {}/{}".format(second_schedl, done_tasksets))

        print ("third schedulable: {}/{}".format(third_schedl, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - first_schedl - second_schedl - third_schedl), done_tasksets))


    print ("first schedulable: {}/{}".format(first_schedl, no_tasksets))

    print ("second schedulable: {}/{}".format(second_schedl, no_tasksets))

    print ("third schedulable: {}/{}".format(third_schedl, no_tasksets))

    total_sched_able = (first_schedl + second_schedl + third_schedl)
    avge2e = 0
    if total_sched_able:
        avge2e = int(float(e2e_delay_sum) / total_sched_able)

    with open("accepted_waters_copi.txt", "a") as f:
        f.write("{} ".format(total_sched_able))

    with open("accepted_waters_avge2e.txt", "a") as f:
        f.write("{} ".format(avge2e))

    avg_accept_time = 0
    if (total_sched_able > 0):
        avg_accept_time = int(1000 * float(sum(accepted_time_taken)) / total_sched_able)
    print ("Average Accepted Time Taken: ", avg_accept_time, "ms")

    with open("accepted_time_waters.txt", "a") as f:
        f.write("{} ".format(avg_accept_time))

    if total_sched_able < no_tasksets:
        avg_failed_time = int(1000 * float(sum(rejected_time_taken)) / (no_tasksets - total_sched_able))

        print ("Average Rejected Time Taken: ", avg_failed_time, "ms")

        with open("failed_time_waters.txt", "a") as f:
            f.write("{} ".format(avg_failed_time))

    print ("Unschedulable: {}/{}".format((no_tasksets - total_sched_able), no_tasksets))
    print ("Loss Rate: ", Loss_Rate, "E2E Factor:", e2e_delay_factor)

if __name__ == "__main__":
    main(sys.argv[1:])
