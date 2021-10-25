import task_generator as task_gen
from utility import *
from pipeline import *
import os, pickle, sys
import numpy as np
from pipeline import *
from timeit import default_timer as timer

from gekko import GEKKO

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

under_75 = 0
under_50 = 0
under_25 = 0
under_0  = 0

def solve_gekko(budgets, e2e_delay_threshold, Loss_UB = 1):
    global glob_budgets, under_0, under_25, under_50, under_75
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
        periods.append(m.Var(value = (budgets[i] * 400), lb = int(budgets[i] * 1.5), ub = budgets[i] * 20000, integer = True))
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
    # m.Equation(loss_rate_ub_GEKKO(taskset, budgets, m) <= 0.75)

    # m.Obj(end_to_end_delay_durr_periods(periods, m))
    # m.Obj(sum(periods))
    # m.Obj(loss_rate_ub_GEKKO(taskset, budgets, m))
    m.Equation(loss_rate_ub_GEKKO(taskset, budgets, m) <= Loss_UB)
    try:
        m.solve(disp=False)
        # print("GEKKO ", m.options.objfcnval)
        # final_taskset = [(budgets[i], periods[i].value[0]) for i in range(len(budgets))]
        # lr = loss_rate_ub(final_taskset, budgets)
        # print (final_taskset, lr)
        # if lr <= 0:
        #     under_0 += 1
        # if lr <= 0.25:
        #     under_25 += 1
        # if lr <= 0.50:
        #     under_50 += 1
        # if lr <= 0.75:
        #     under_75 += 1

        return m, periods
    except:
        return (None, None)

def main():
    Loss_UB = 1
    accepted_time_taken = []
    rejected_time_taken = []

    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 15

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

        start = timer()
        solution, periods = solve_gekko(budgets, e2e_delay_threshold, Loss_UB = 0.75)
        end = timer()
        if solution is not None:
            periods = [x.value[0] for x in periods]
            if solution.options.SOLVESTATUS == 1:
                accepted_time_taken.append((end - start))
                print ("GEKKO E2E: ", end_to_end_delay_durr_periods_orig(periods))
                # print (periods, "e2e: ", solution.options.objfcnval, end_to_end_delay_durr_periods_orig(periods), get_total_util_2(budgets, periods))
                # cur_loss_rate = loss_rate_ub(taskset)
                # print ("LR: ", cur_loss_rate * 100)
                # if(loss_rate_ub(taskset) <= Loss_UB):
                schedulable += 1
            else:
                rejected_time_taken.append((end - start))
        else:
            rejected_time_taken.append((end - start))


        done_tasksets += 1
        print ("Schedulable: {}/{}".format(schedulable, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - schedulable), done_tasksets))

    print ("Schedulable: {}/{}".format(schedulable, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

    print ("Average Accepted Time Taken: ", int(1000 * float(sum(accepted_time_taken)) / schedulable), "ms")

    print ("Average Rejected Time Taken: ", float(sum(rejected_time_taken)) / (no_tasksets - schedulable))

    print ("E2E Factor:", e2e_delay_factor)

    print ("under_0, under_25, under_50, under_75: ", under_0, under_25, under_50, under_75)

if __name__ == "__main__":
    main()
