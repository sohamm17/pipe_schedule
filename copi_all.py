'''
-- This is for Loss Rate experiment.
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

Loss_Rate = 50 # In Percentage
Loss_UB = float(Loss_Rate) / 100

def optimize_alpha(single_set, budgets, equal_period, e2e_delay, starting_alpha=1.7):
    global Loss_Rate, Loss_UB
    alpha = starting_alpha
    step = 0.01
    schedulable = False
    initial_budgets = budgets

    # Main Loop consisting of Stage 2 and 3
    while alpha > 1.0 and not schedulable:
        # print ("NEW ITER")
        increased_period = int(alpha * equal_period)

        taskset = [(b, increased_period) for b in budgets]
        # print ("Scaled alpha: ", taskset, alpha, end_to_end_delay_durr(taskset), loss_rate_ub(taskset, initial_budgets), get_total_util(taskset) * 100)

        is_second_stage_sched = False

        # the following variable keeps track of whether at least one pipe was changed.
        at_least_one_pipe_changed = False
        # print ("\nNew Iter Second Stage: ", taskset, "bound:", e2e_delay, end_to_end_delay_durr(taskset), alpha, get_total_util(taskset))
        while True:
            # print ("SECOND STEP")
            i = 0
            while i < len(taskset) - 1:
                producer = taskset[i]
                consumer = taskset[i + 1]

                # print ("Iter ", i, taskset, end_to_end_delay_durr(taskset), loss_rate_ub(taskset, initial_budgets), get_total_util(taskset) * 100)
                taskset2 = copy.deepcopy(taskset)

                if producer[0] < (producer[1] // 2) and consumer[0] * 2 < consumer[1]:
                    # period of the producer is halved
                    producer = (producer[0], producer[1] // 2)
                    # budget of the consumer is doubled
                    consumer = (consumer[0] * 2, consumer[1])
                    taskset2[i] = producer
                    taskset2[i + 1] = consumer

                    if utilization_bound_test(taskset2):
                        # print ("2nd U:", get_total_util(taskset2), end_to_end_delay_durr(taskset2), loss_rate_ub(taskset2, budgets))
                        # print (taskset2)
                        taskset = copy.deepcopy(taskset2)
                        # taskset = make_taskset_harmonic(taskset)
                        at_least_one_pipe_changed = True
                        # Skip the next task because it is tuned
                        # i += 1 # Loss Rate Optimizer
                        # print ("S:", taskset, loss_rate_ub(taskset, initial_budgets), i)
                        # print (taskset, get_total_util(taskset))

                        if end_to_end_delay_durr(taskset) <= e2e_delay and loss_rate_ub(taskset, initial_budgets) <= Loss_UB:
                            # print ("Under e2e_delay threshold")
                            # print (taskset)
                            # print ("Second Stage Sched, E2E: ", end_to_end_delay_durr(taskset))
                            # print (taskset)
                            schedulable = True
                            is_second_stage_sched = True
                            return 2 # Second stage Schedulable
                i += 1
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
        # print ("Third Stage", taskset)

        #Stage 3
        if utilization_bound_test(taskset):
            # print ("Third Stage Entry: ", taskset, end_to_end_delay_durr(taskset), loss_rate_ub(taskset, initial_budgets), get_total_util(taskset) * 100)
            # print (initial_budgets)
            # print ("LR: ", loss_rate_ub(taskset, initial_budgets) * 100)
            for i in range(len(taskset) - 1, -1, -1):
                # print (i)
                cur_budget = int(taskset[i][0])
                cur_period = int(taskset[i][1])

                initial_budget = int(single_set[i][0])
                # print (cur_budget, cur_period, initial_budget)

                while cur_budget // 2 >= initial_budget:
                    cur_budget = cur_budget // 2
                    cur_period = cur_period // 2
                    # print ("Halved budget and period", i + 1)
                    # taskset[i] = (cur_budget, cur_period)
                    # print (taskset, end_to_end_delay_durr(taskset), loss_rate_ub(taskset, initial_budgets), get_total_util(taskset) * 100)

                taskset[i] = (cur_budget, cur_period)

                # print ("3rd U:", get_total_util(taskset), end_to_end_delay_durr(taskset), loss_rate_ub(taskset, budgets))

                if utilization_bound_test(taskset) and end_to_end_delay_durr(taskset) <= e2e_delay:
                    # print ("Third Stage Schedulable and under threshold")
                    # print (taskset, end_to_end_delay_durr(taskset), 100 * get_total_util(taskset))
                    cur_loss_rate = loss_rate_ub(taskset, initial_budgets)
                    # print ("LR: ", cur_loss_rate * 100, max(budgets), min(budgets))
                    # print (taskset, end_to_end_delay_durr(taskset), loss_rate_ub(taskset, initial_budgets), get_total_util(taskset) * 100)
                    # sys.exit(1)
                    if(cur_loss_rate <= Loss_UB):
                        schedulable = True
                        prompt = 1
                        if (cur_loss_rate == 0):
                            input(prompt)
                        return 3
                    # else:
                    #     sys.exit(1)
                elif end_to_end_delay_durr(taskset) <= e2e_delay:
                    harm_taskset = make_taskset_harmonic(taskset)
                    taskset = harm_taskset
                    if utilization_bound_test(taskset) and end_to_end_delay_durr(taskset) <= e2e_delay:
                        cur_loss_rate = loss_rate_ub(taskset, initial_budgets)
                        # print ("LR: ", cur_loss_rate * 100)
                        # print (harm_taskset, initial_budgets)
                        # sys.exit(1)
                        if(cur_loss_rate <= Loss_UB):
                            schedulable = True
                            # sys.exit(1)
                            return 3

            # print (taskset)
        alpha = alpha - step

    return 0

def main(argv):
    global Loss_Rate, Loss_UB
    accepted_num_iterations = []
    accepted_time_taken = []
    rejected_time_taken = []
    Loss_UB = -1
    e2e_delay_factor = -1

    # Taking arguments

    usage = 'Usage: python copi_all.py -l <loss_rate> -e <LBG>'

    try:
        opts, args = getopt.getopt(argv, "l:e:")
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            Loss_UB = float(arg)
            if Loss_UB > 1:
                print ("loss_rate cannot be more than 1. cannot proceed.")
                sys.exit(2)
        elif opt == '-e':
            e2e_delay_factor = float(arg)

    if Loss_UB == -1:
        print ("Loss Rate UB is not provided.")
        print (usage)
        sys.exit(2)

    if e2e_delay_factor == -1:
        print ("E2E Delay UB in the form of Latency Budget Gap (LBG) is not provided.")
        print ('Usage: python opt_s2_lr.py -l <loss_rate> -e <e2e delay factor>')
        sys.exit(2)

    Loss_Rate = int(100 * Loss_UB)

    random.seed(50)
    no_tasks = 5
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

        if utilization_bound_test(taskset) and end_to_end_delay_durr(taskset) <= e2e_delay_ub and loss_rate_ub(taskset, budgets) <= Loss_UB:
            # print (get_total_util(taskset))
            first_schedl += 1
            done_tasksets += 1
            opt_alpha = 1
        else:
            # print ("Second Stage", taskset, get_total_util(taskset))

            #Step 2
            opt_alpha = optimize_alpha(single_set, budgets, equal_period, e2e_delay_ub, starting_alpha = 2)
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
    with open("result_lr_copi.txt", "a") as f:
        f.write("{} ".format(total_sched_able))

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
