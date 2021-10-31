'''
-- This is more optimized version to make tasksets harmonic
'''

import task_generator as task_gen

import numpy as np
import math
import matplotlib.pyplot as plt
import sys, os, pickle, getopt
from utility import *
from pipeline import *
import copy, random
from timeit import default_timer as timer

num_iterations = 0

def optimize_alpha(single_set, budgets, equal_period, e2e_delay, starting_alpha=1.7, ending_alpha=2.0):
    global num_iterations
    num_iterations = 0
    alpha = starting_alpha
    step = 0.01
    schedulable = False
    # print ("------", sum(budgets), e2e_delay, (float(e2e_delay) / sum(budgets)) / len(budgets))

    while alpha <= ending_alpha and not schedulable:
        increased_period = int(alpha * equal_period)

        taskset = [(b, increased_period) for b in budgets]

        is_second_stage_sched = False

        # the following variable keeps track of whether at least one pipe was changed.
        at_least_one_pipe_changed = False

        # If a stretched Pipeline is not schedulable then break
        # if not utilization_bound_test(taskset):
        #     break

        num_iterations += 1

        while True:
            for i in range(0, len(taskset) - 1):
                producer = taskset[i]
                consumer = taskset[i + 1]

                # print ("Iter ", i, taskset)
                taskset2 = copy.deepcopy(taskset)

                if producer[0] < (producer[1] // 2) and consumer[0] * 2 < consumer[1]:
                    # period of the producer is halved
                    producer = (producer[0], producer[1] // 2)
                    # budget of the consumer is doubled
                    consumer = (consumer[0] * 2, consumer[1])
                    taskset2[i] = producer
                    taskset2[i + 1] = consumer

                    if utilization_bound_test(taskset2):
                        taskset = copy.deepcopy(taskset2)
                        # print ("2nd U:", get_total_util(taskset2), end_to_end_delay_durr(taskset2), loss_rate_ub(taskset, budgets))
                        # print (taskset2)
                        at_least_one_pipe_changed = True
                        # i += 1
                        # print (taskset, get_total_util(taskset))
                        if end_to_end_delay_durr(taskset) <= e2e_delay:
                            # print ("Under e2e_delay threshold")
                            # print (taskset)
                            schedulable = True
                            is_second_stage_sched = True
                            # print ("Second Stage Sched, E2E: ", end_to_end_delay_durr(taskset))
                            # print (taskset)
                            return 2 # Second stage Schedulable
            # if it is already schedulable do not tune another task
            if is_second_stage_sched:
                break
            elif not at_least_one_pipe_changed:
                break
            elif at_least_one_pipe_changed:
                #change back the value to false
                at_least_one_pipe_changed = False

        if is_second_stage_sched:
            break

        # Third Stage
        if utilization_bound_test(taskset):
            # print ("Third Stage", taskset)

            #Step 5
            for i in range(len(taskset) - 1, -1, -1):
                cur_budget = int(taskset[i][0])
                cur_period = int(taskset[i][1])

                initial_budget = int(single_set[i][0])
                # print (cur_budget, cur_period, initial_budget)

                while cur_budget // 2 >= initial_budget:
                    cur_budget = cur_budget // 2
                    cur_period = cur_period // 2
                    # print ("Halved budget and period")

                taskset[i] = (cur_budget, cur_period)

                if utilization_bound_test(taskset) and end_to_end_delay_durr(taskset) <= e2e_delay:
                    # print ("Third Stage Schedulable and under threshold")
                    # print (taskset, end_to_end_delay_durr(taskset), 100 * get_total_util(taskset))
                    schedulable = True
                    # print ("Scheduling Alpha: :", alpha)
                    # sys.exit(1)
                    return 3
        alpha = alpha + step

    return 0

def main(argv):
    global num_iterations
    accepted_num_iterations = []
    accepted_time_taken = []
    rejected_time_taken = []
    no_tasks = -1
    nlbg = 1.5
    usage = 'Usage: python copi_e2e.py -n <number of tasks> -x <NLBG, default is 1.5>'

    try:
        opts, args = getopt.getopt(argv, "n:x:")
    except getopt.GetoptError:
        print (usage)
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-n':
            no_tasks = int(arg)
        if opt == '-x':
            nlbg = float(arg)

    if no_tasks < 1:
        print ("Number of tasks is missing.")
        print (usage)
        sys.exit(1)

    if nlbg < 1:
        print ("NLBG should be more than 1.")
        print (usage)
        sys.exit(1)

    print (f"NLBG = {nlbg:.2f}")

    no_tasksets = 1000

    total_util = 0.75

    e2e_delay_factor = no_tasks * nlbg #LBG

    min_period = 100
    max_period = 1000

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)
    # sys.exit(1)

    first_schedl = 0
    second_schedl = 0
    third_schedl = 0

    setfile_string = "percent_" + str(total_util) + "_" + str(no_tasks)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    done_tasksets = 0
    for single_set in current_sets:
        opt_alpha = 0
        num_iterations = 0
        budgets = [x[0] for x in single_set]
        periods = [x[1] for x in single_set]

        # budgets = [random.randint(5, 250) for x in single_set]
        # print (budgets)
        # single_set = [(budgets[i], periods[i]) for i in range(len(single_set))]
        # print ("max/min budget:", max(budgets)/min(budgets))

        # we calculate end_to_end delay_ub as a factor of the summation of budgets
        e2e_delay_ub = int(sum(budgets) * e2e_delay_factor)
        print ("Sum Budgets: {}, E2E_UB: {}".format(sum(budgets), e2e_delay_ub))

        alpha_cal = float(sum(budgets)) / float(e2e_delay_ub) *  (1 / (pow(2, 1.0 / no_tasks) - 1)) * ((no_tasks + 1) / no_tasks)
        print ("alpha_cal {}".format(alpha_cal))

        start = timer()
        equal_period = int(e2e_delay_ub / (no_tasks + 1))
        # for b in budgets:
        #     if b > equal_period:
        #         print ("Not schedulable: ", single_set, equal_period)
        #         sys.exit(0)

        #Step 1
        taskset = [(b, equal_period) for b in budgets]

        if utilization_bound_test(taskset) and end_to_end_delay_durr(taskset) <= e2e_delay_ub:
            # print ("First: ", taskset, end_to_end_delay_durr(taskset), get_total_util(taskset))
            first_schedl += 1
            opt_alpha = 1
        #Step 2
        else:
            opt_alpha = optimize_alpha(single_set, budgets, equal_period, e2e_delay_ub, starting_alpha = alpha_cal, ending_alpha = 2)

            if opt_alpha == 2:
                second_schedl += 1
            elif opt_alpha == 3:
                third_schedl += 1

        end = timer()

        if opt_alpha > 1:
            accepted_time_taken.append((end - start))
            accepted_num_iterations.append(num_iterations)
            print ("Alpha cal: :", alpha_cal)
        elif opt_alpha < 1:
            rejected_time_taken.append((end - start))

        done_tasksets += 1
        print ("{} Completed Tasksets.".format(done_tasksets))
        print ("first schedulable: {}/{}".format(first_schedl, done_tasksets))

        print ("second schedulable: {}/{}".format(second_schedl, done_tasksets))

        print ("third schedulable: {}/{}".format(third_schedl, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - first_schedl - second_schedl - third_schedl), done_tasksets))
        # if done_tasksets >= 200:
        #     break


    print ("first schedulable: {}/{}".format(first_schedl, no_tasksets))

    print ("second schedulable: {}/{}".format(second_schedl, no_tasksets))

    print ("third schedulable: {}/{}".format(third_schedl, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - first_schedl - second_schedl - third_schedl), no_tasksets))

    total_sched_able = (first_schedl + second_schedl + third_schedl)

    print ("Average Num Iteration for Accepted: ", float(sum(accepted_num_iterations)) / total_sched_able)

    avg_accept_time = int(1000 * float(sum(accepted_time_taken)) / total_sched_able)
    print ("Average Accepted Time Taken: ", avg_accept_time, "ms")

    if total_sched_able < no_tasksets:
        avg_failed_time = int(1000 * float(sum(rejected_time_taken)) / (no_tasksets - total_sched_able))

        with open("failed_time.txt", "a") as f:
            f.write("{} ".format(avg_failed_time))

        print ("Average Rejected Time Taken: ", avg_failed_time, "ms")

    print ("E2E Factor:", e2e_delay_factor, "NLBG:", nlbg, "no tasks:", no_tasks)

    with open("accepted_time.txt", "a") as f:
        f.write("{} ".format(avg_accept_time))

if __name__ == "__main__":
    main(sys.argv[1:])
