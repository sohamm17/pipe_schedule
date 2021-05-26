import task_generator as task_gen
from utility import *
from pipeline import *
import os, pickle, sys
import numpy as np
from pipeline import *

from gekko import GEKKO

Loss_Rate = 50 # In Percentage
Loss_UB = float(Loss_Rate) / 100

glob_budgets =[]

def total_util(periods):
    global glob_budgets
    sum = 0
    for i in range(len(periods)):
        sum += float(glob_budgets[i])/periods[i].value
    print (periods, sum)
    return (100 * sum)

def sample_sums(periods):
    print (periods, sum(periods))
    return sum(periods)

def solve_gekko(budgets, e2e_delay_threshold):
    global glob_budgets
    no_tasks = len(budgets)

    m = GEKKO(remote=False) # Initialize gekko

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
        periods.append(m.Var(value = (e2e_delay_threshold / (no_tasks + 1)), lb = int(budgets[i] * 1.5), ub = budgets[i] * 20000, integer = True))
        # periods.append(m.Var(value = 5, lb = 0, ub = 10, integer = True))
        # Increasing Period Constraint
        # if i > 0:
        #     m.Equation(periods[i] >= periods[i - 1])

    glob_budgets = budgets

    taskset = []
    for i in range(len(budgets)):
        taskset.append((budgets[i], periods[i]))

    m.Equation(end_to_end_delay_durr_periods(periods, m)<=e2e_delay_threshold)
    m.Equation(utilization_bound_gekko(taskset, m, periods)>= 0.0)

    # m.Obj(end_to_end_delay_durr_periods(periods, m))
    # m.Obj(sum(periods))
    m.Obj(loss_rate_ub_GEKKO(taskset, budgets, m))
    try:
        m.solve(disp=False)
        print("GEKKO ", m.options.objfcnval)
        for p in periods:
            print (p.value)

        return m, periods
    except:
        return (None, None)

def main():
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 16

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    schedulable = 0

    setfile_string = "../percent_" + str(total_util) + "_" + str(no_tasks)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    done_tasksets = 0
    for single_set in current_sets:
        budgets = [x[0] for x in single_set]

        e2e_delay_threshold = int(sum(budgets) * e2e_delay_factor)
        print ("E2E Threshold = ", e2e_delay_threshold)

        solution, periods = solve_gekko(budgets, e2e_delay_threshold)
        if solution is not None:
            periods = [x.value[0] for x in periods]
            if solution.options.SOLVESTATUS == 1:
                print ("GEKKO E2E: ", end_to_end_delay_durr_periods_orig(periods))
                # print (periods, "e2e: ", solution.options.objfcnval, end_to_end_delay_durr_periods_orig(periods), get_total_util_2(budgets, periods))
                # cur_loss_rate = loss_rate_ub(taskset)
                # print ("LR: ", cur_loss_rate * 100)
                # if(loss_rate_ub(taskset) <= Loss_UB):
                schedulable += 1

        done_tasksets += 1
        print ("Schedulable: {}/{}".format(schedulable, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - schedulable), done_tasksets))

    print ("Schedulable: {}/{}".format(schedulable, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

    print ("E2E Factor:", e2e_delay_factor)

if __name__ == "__main__":
    main()
