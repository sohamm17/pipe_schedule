"""
This file is used by the multiprocessor multi-pipeline algorithm.
"""
import task_generator as task_gen

import numpy as np
import math
import matplotlib.pyplot as plt
import sys, os, pickle, copy
from utility import *
from pipeline import *

from gekko import GEKKO

"""
try_util_bound: It is to try get the util under a suggested bound.
"""
GEKKO_RUN = False

def optimize_alpha_live(budgets, e2e_delay, loss_rate_bound, try_util_bound, starting_alpha=1.7):
    if GEKKO_RUN:
        return solve_gekko(budgets, e2e_delay, loss_rate_bound, try_util_bound)

    no_tasks = len(budgets)

    equal_period = int(e2e_delay / (no_tasks + 1))
    taskset = [(b, equal_period) for b in budgets]
    # print (get_total_util(taskset))
    # print (sum(budgets), e2e_delay, (float(e2e_delay) / sum(budgets)) / no_tasks)

    if get_total_util(taskset) <= try_util_bound and end_to_end_delay_durr(taskset) <= e2e_delay and loss_rate_ub(taskset, budgets) <= loss_rate_bound:
        # print("Simple", get_total_util(taskset))
        return taskset, 1

    alpha = starting_alpha
    step = 0.01
    schedulable = False
    suggested_pipeline = None

    while alpha > 1.15 and not schedulable:
        increased_period = int(alpha * equal_period)

        taskset = [(b, increased_period) for b in budgets]
        # print ("stretched:", taskset, get_total_util(taskset), try_util_bound)
        if get_total_util(taskset) > try_util_bound:
            break
        # the following variable keeps track of whether at least one pipe was changed.
        at_least_one_pipe_changed = False
        did_stage2_work = False

        # print ("\nITER ", e2e_delay, loss_rate_bound, taskset, alpha, end_to_end_delay_durr(taskset), get_total_util(taskset))
        while True:
            i = 0
            while i < (len(taskset) - 1):
                taskset2 = copy.deepcopy(taskset)
                producer = taskset2[i]
                consumer = taskset2[i + 1]

                # print ("Iter ", i, taskset)

                if producer[0] < (producer[1] // 2) and consumer[0] * 2 < consumer[1]:
                    # period of the producer is halved
                    producer = (producer[0], producer[1] // 2)
                    # budget of the consumer is doubled
                    consumer = (consumer[0] * 2, consumer[1])
                    taskset2[i] = producer
                    taskset2[i + 1] = consumer

                    if get_total_util(taskset2) <= try_util_bound:
                        # print ("2nd U:", get_total_util(taskset2), end_to_end_delay_durr(taskset2), loss_rate_ub(taskset2, budgets))
                        # print (taskset2)
                        taskset = copy.deepcopy(taskset2)
                        taskset = make_taskset_harmonic(taskset)
                        i += 1 #- skip for successful ones
                        at_least_one_pipe_changed = True
                        # previously, we used the duur equation, but
                        # we have to use davare equation to avoid
                        # task priority dependency
                        if end_to_end_delay_davare(taskset) <= e2e_delay and loss_rate_ub(taskset, budgets) <= loss_rate_bound:
                        # if end_to_end_delay_durr(taskset) <= e2e_delay and loss_rate_ub(taskset, budgets) <= loss_rate_bound:
                            schedulable = True
                            print ("Second Stage Sched, E2E: ", end_to_end_delay_durr(taskset), loss_rate_ub(taskset, budgets), get_total_util(taskset))
                            print (taskset)
                            return taskset, 2
                i += 1
            if not at_least_one_pipe_changed:
                break
            elif at_least_one_pipe_changed:
                did_stage2_work = True
                #change back the value to false
                at_least_one_pipe_changed = False

        # Third Stage

        #Step 5
        if did_stage2_work and get_total_util(taskset) <= try_util_bound:
            # print ("Util After Stage2:", get_total_util(taskset), taskset)
            # print ("Third Stage Entry: ", taskset, get_total_util(taskset), end_to_end_delay_durr(taskset))
            # print ("LR: ", loss_rate_ub(taskset, budgets) * 100)
            for i in range(len(taskset) - 1, -1, -1):
                cur_budget = int(taskset[i][0])
                cur_period = int(taskset[i][1])

                initial_budget = int(budgets[i])
                # print (cur_budget, cur_period, initial_budget)

                while cur_budget // 2 >= initial_budget:
                    cur_budget = cur_budget // 2
                    cur_period = cur_period // 2

                # print ("3rd U:", get_total_util(taskset), end_to_end_delay_durr(taskset), loss_rate_ub(taskset, budgets))

                taskset[i] = (cur_budget, cur_period)
                taskset = make_taskset_harmonic(taskset)
                # print ("After Third Stage: ", end_to_end_delay_durr(taskset), loss_rate_ub(taskset, budgets), get_total_util(taskset))
                # print (taskset)
                if end_to_end_delay_durr(taskset) <= e2e_delay and loss_rate_ub(taskset, budgets) <= loss_rate_bound:
                    print ("Optimized")
                    return taskset, 2
        alpha = alpha - step

    return None, None

"""
Live Gekko Optimization
"""
def solve_gekko(budgets, e2e_delay_threshold, loss_rate_ub, try_util_bound):
    # global glob_budgets
    no_tasks = len(budgets)

    m = GEKKO(remote=False) # Initialize gekko
    print (sum(budgets), e2e_delay_threshold)

    # APOPT Solver
    m.options.SOLVER=1  # APOPT is an MINLP solver
    # optional solver settings with APOPT
    m.solver_options = ['minlp_maximum_iterations 70000', \
    # minlp iterations with integer solution
    'minlp_max_iter_with_int_sol 5000', \
    # treat minlp as nlp
    'minlp_as_nlp 0', \
    # nlp sub-problem max iterations
    'nlp_maximum_iterations 2000', \
    # 1 = depth first, 2 = breadth first
    'minlp_branch_method 1', \
    # maximum deviation from whole number
    'minlp_integer_tol 0.5', \
    # covergence tolerance
    'minlp_gap_tol 0.1']

    periods = []
    prios = []

    for i in range(no_tasks):
        periods.append(m.Var(value = (budgets[i] * 15000), lb = int(budgets[i] * 1.5), ub = budgets[i] * 20000, integer = True))
        # periods.append(m.Var(value = 5, lb = 0, ub = 10, integer = True))
        # Increasing Period Constraint
        # if i > 0:
        #     m.Equation(periods[i] >= periods[i - 1])

    # glob_budgets = budgets

    taskset = []
    for i in range(len(budgets)):
        taskset.append((budgets[i], periods[i]))

    m.Equation(end_to_end_delay_durr_periods(periods, m)<=e2e_delay_threshold)
    m.Equation(utilization_bound_gekko(taskset, m, periods)>= 0.0)

    # m.Obj(end_to_end_delay_durr_periods(periods, m))
    # m.Obj(sum(periods))
    try:
        print ("GEKKO Trying")
        m.solve(disp=False)
        final_taskset = [(budgets[i], periods[i].value) for i in range(len(budgets))]

        print("GEKKO LR: ", loss_rate_ub(final_taskset))

        if loss_rate_ub(final_taskset) <= loss_rate_ub and end_to_end_delay_durr(taskset) <= e2e_delay_threshold and get_total_util(taskset) <= try_util_bound:
            return final_taskset, 2
        else:
            return (None, None)
    except:
        return (None, None)
