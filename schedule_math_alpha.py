'''


I derive an alpha value from mathematical equation
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

def main():
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 1
    alpha = 1.1

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    first_schedl = 0
    second_schedl = 0
    third_schedl = 0

    setfile_string = "dataset_" + str(total_util)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    for single_set in current_sets:
        budgets = [x[0] for x in single_set]
        periods = [x[1] for x in single_set]

        e2e_delay = int(sum(periods) * float(e2e_delay_factor))

        equal_period = e2e_delay // no_tasks
        for b in budgets:
            if b > equal_period:
                print ("Not schedulable: ", single_set, equal_period)
                # sys.exit(0)

        #Step 1
        taskset = [(b, equal_period) for b in budgets]

        if utilization_bound_test(taskset):
            first_schedl += 1
            continue

        print ("e2e delay threshold=", e2e_delay)
        print ("Second Stage", taskset, get_total_util(taskset))
        print ("Budget sum / e2edelay = ", (float(sum(budgets))/float(e2e_delay)))

        alpha = float(sum(budgets)) / (float(e2e_delay) * ((pow(2, 1.0 / len(taskset)) - 1 - 0.01)))

        print ("Sum of budgets=", sum(budgets))
        print ("Derived Alpha = ", alpha)

        #Step 2
        increased_period = int(alpha * equal_period)

        taskset = [(b, increased_period) for b in budgets]
        print ("Special Alpha ", taskset)
        print ("e2e delay: ", end_to_end_delay(taskset))

        if utilization_bound_test(taskset) and end_to_end_delay(taskset) <= e2e_delay:
            print ("Found a special alpha")
            second_schedl += 1
            continue

        #Step 3
        is_second_stage_sched = False
        for i in range(0, len(taskset) - 1):
            producer = taskset[i]
            consumer = taskset[i + 1]

            print ("Iter ", i, taskset)
            taskset2 = copy.deepcopy(taskset)

            while producer[0] < producer[1] and consumer[0] < consumer[1]:
                # period of the producer is halved
                producer = (producer[0], producer[1] // 2)
                # budget of the consumer is doubled
                consumer = (consumer[0] * 2, consumer[1])
                taskset2[i] = producer
                taskset2[i + 1] = consumer

                if utilization_bound_test(taskset2):
                    taskset = copy.deepcopy(taskset2)
                else:
                    break

                print (taskset, get_total_util(taskset))

                if end_to_end_delay(taskset) <= e2e_delay:
                    # print ("Under e2e_delay threshold")
                    # print (taskset)
                    second_schedl += 1
                    is_second_stage_sched = True
                    break

            # if it is already schedulable do not tune another task
            if is_second_stage_sched:
                break

        if is_second_stage_sched:
            print ("Second stage scheduled: ", taskset)
            continue

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
                third_schedl += 1
                print ("Third stage scheduled: ", taskset)
                break

            print (taskset)

        # sys.exit(0)


    print ("first schedulable: {}/{}".format(first_schedl, no_tasksets))

    print ("second schedulable: {}/{}".format(second_schedl, no_tasksets))

    print ("third schedulable: {}/{}".format(third_schedl, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - first_schedl - second_schedl - third_schedl), no_tasksets))

if __name__ == "__main__":
    main()
