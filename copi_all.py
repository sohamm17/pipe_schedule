'''
-- This is for the Loss Rate experiment.
End-to-end delay and utilization bound constraint is always there.
'''
import task_generator as task_gen
from copi_lib import *

import numpy as np
import math
import matplotlib.pyplot as plt
import sys, os, pickle, getopt
from utility import *
from pipeline import *
import random
from timeit import default_timer as timer

def main(argv):
    Loss_Rate = 50 # In Percentage
    loss_ub = float(Loss_Rate) / 100
    accepted_num_iterations = []
    accepted_time_taken = []
    rejected_time_taken = []
    loss_ub = -1
    e2e_delay_factor = -1
    no_tasks = -1

    # Taking arguments

    usage = 'Usage: python copi_all.py -n <no of tasks> -l <loss_rate> -e <LBG>'

    try:
        opts, args = getopt.getopt(argv, "n:l:e:")
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            loss_ub = float(arg)
            if loss_ub > 1:
                print ("loss_rate cannot be more than 1. cannot proceed.")
                sys.exit(1)
        elif opt == '-e':
            e2e_delay_factor = float(arg)
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

    if e2e_delay_factor == -1:
        print ("E2E Delay UB in the form of Latency Budget Gap (LBG) is not provided.")
        print (usage)
        sys.exit(1)

    Loss_Rate = int(100 * loss_ub)

    random.seed(50)
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75 # Just to generate a distribution by UUnifast

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    first_schedl = 0
    second_schedl = 0
    third_schedl = 0

    setfile_string = "dataset_" + str(total_util) + "_" + str(no_tasks)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    done_tasksets = 0
    for single_set in current_sets:
        print ("single_set:", single_set)
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
            done_tasksets += 1
            opt_alpha = 1
        else:
            # print ("Second Stage", taskset, get_total_util(taskset))

            #Step 2
            opt_alpha = optimize_alpha_all(single_set, budgets, equal_period, e2e_delay_ub, loss_ub, starting_alpha = 2)
            # if opt_alpha > 1:
            #     print ("max, min:", max(budgets), min(budgets))

            if opt_alpha == 2:
                second_schedl += 1
            elif opt_alpha == 3:
                third_schedl += 1

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
    with open("accepted_lr_copi.txt", "a") as f:
        f.write("{} ".format(total_sched_able))

    avg_accept_time = 0
    if (total_sched_able > 0):
        avg_accept_time = int(1000 * float(sum(accepted_time_taken)) / total_sched_able)
    print ("Average Accepted Time Taken: ", avg_accept_time, "ms")

    with open("accepted_time_lr.txt", "a") as f:
        f.write("{} ".format(avg_accept_time))

    if total_sched_able < no_tasksets:
        avg_failed_time = int(1000 * float(sum(rejected_time_taken)) / (no_tasksets - total_sched_able))

        print ("Average Rejected Time Taken: ", avg_failed_time, "ms")

        with open("failed_time_lr.txt", "a") as f:
            f.write("{} ".format(avg_failed_time))

    print ("Unschedulable: {}/{}".format((no_tasksets - total_sched_able), no_tasksets))
    print ("Loss Rate: ", Loss_Rate, "E2E Factor:", e2e_delay_factor)

if __name__ == "__main__":
    main(sys.argv[1:])
