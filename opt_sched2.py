'''
The Boomerang Scheduler Simulation
In this one, I try Stage 2 one pipe only once and apply sequentially from first producer to last consumer and then come back again.
'''

import task_generator as task_gen

import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import os
import pickle
from utility import *
import copy

def optimize_alpha(single_set, budgets, equal_period, e2e_delay, starting_alpha=1.7):
    alpha = starting_alpha
    step = 0.01
    schedulable = False

    while alpha > 1.0 and not schedulable:
        increased_period = int(alpha * equal_period)

        taskset = [(b, increased_period) for b in budgets]

        is_second_stage_sched = False

        # the following variable keeps track of whether at least one pipe was changed.
        at_least_one_pipe_changed = False

        while True:
            for i in range(0, len(taskset) - 1):
                producer = taskset[i]
                consumer = taskset[i + 1]

                print ("Iter ", i, taskset)
                taskset2 = copy.deepcopy(taskset)

                if producer[0] < producer[1] and consumer[0] < consumer[1]:
                    # period of the producer is halved
                    producer = (producer[0], producer[1] // 2)
                    # budget of the consumer is doubled
                    consumer = (consumer[0] * 2, consumer[1])
                    taskset2[i] = producer
                    taskset2[i + 1] = consumer

                    if utilization_bound_test(taskset2):
                        taskset = copy.deepcopy(taskset2)
                        at_least_one_pipe_changed = True
                        print (taskset, get_total_util(taskset))

                    if end_to_end_delay(taskset) <= e2e_delay:
                        # print ("Under e2e_delay threshold")
                        # print (taskset)
                        schedulable = True
                        is_second_stage_sched = True
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
        print ("Third Stage", taskset)

        #Step 5
        for i in range(len(taskset) - 1, -1, -1):
            cur_budget = int(taskset[i][0])
            cur_period = int(taskset[i][1])

            initial_budget = int(single_set[i][0])
            print (cur_budget, cur_period, initial_budget)

            while cur_budget < cur_period and cur_budget > initial_budget:
                cur_budget = cur_budget // 2
                cur_period = cur_period // 2
                # print ("Halved budget and period")

            taskset[i] = (cur_budget, cur_period)

            if utilization_bound_test(taskset) and end_to_end_delay(taskset) <= e2e_delay:
                # print ("Schedulable and under threshold")
                # print (taskset)
                schedulable = True
                return 3 # Third Stage Schedulable

            # print (taskset)
        alpha = alpha - step

    return 0

def main():
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 1
    alpha = 1.2

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    first_schedl = 0
    second_schedl = 0
    third_schedl = 0

    setfile_string = "percent_" + str(total_util)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    for single_set in current_sets:
        budgets = [x[0] for x in single_set]
        periods = [x[1] for x in single_set]

        e2e_delay = sum(periods) * e2e_delay_factor

        equal_period = e2e_delay // no_tasks
        for b in budgets:
            if b > equal_period:
                print ("Not schedulable: ", single_set, equal_period)
                sys.exit(0)

        #Step 1
        taskset = [(b, equal_period) for b in budgets]

        if utilization_bound_test(taskset):
            first_schedl += 1
            continue

        print ("Second Stage", taskset, get_total_util(taskset))

        #Step 2
        opt_alpha = optimize_alpha(single_set, budgets, equal_period, e2e_delay, starting_alpha = 1.3)

        if opt_alpha == 2:
            second_schedl += 1
        elif opt_alpha == 3:
            third_schedl += 1


    print ("first schedulable: {}/{}".format(first_schedl, no_tasksets))

    print ("second schedulable: {}/{}".format(second_schedl, no_tasksets))

    print ("third schedulable: {}/{}".format(third_schedl, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - first_schedl - second_schedl - third_schedl), no_tasksets))

if __name__ == "__main__":
    main()
