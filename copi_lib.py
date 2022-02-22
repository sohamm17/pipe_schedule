'''
This file contains all the library files of CoPi
'''
import copy
from utility import *
from pipeline import *

'''
This function solves
'''
def optimize_alpha_all(single_set, budgets, equal_period, e2e_delay, loss_ub, starting_alpha=1.7):
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

                        if end_to_end_delay_durr(taskset) <= e2e_delay and loss_rate_ub(taskset, initial_budgets) <= loss_ub:
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
                    if(cur_loss_rate <= loss_ub):
                        schedulable = True
                        # prompt = 1
                        # if (cur_loss_rate == 0):
                        #     input(prompt)
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
                        if(cur_loss_rate <= loss_ub):
                            schedulable = True
                            # sys.exit(1)
                            return 3

            # print (taskset)
        alpha = alpha - step

    return 0
