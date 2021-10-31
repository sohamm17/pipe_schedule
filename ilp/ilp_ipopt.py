import task_generator as task_gen
from utility import *
import os, pickle

from scipy.optimize import Bounds, minimize, NonlinearConstraint, shgo, LinearConstraint, differential_evolution
import numpy as np

from cyipopt import minimize_ipopt

def e2e_constraint(periods, threshold):
    print ("periods ", periods)
    print ("e2e", end_to_end_delay_durr_periods(periods))
    diff = (threshold - end_to_end_delay_durr_periods(periods))
    return (threshold - end_to_end_delay_durr_periods(periods))

def util_constraint(periods, budgets):
    taskset = []
    # print (budgets)
    for i in range(len(budgets)):
        taskset.append((budgets[i], periods[i]))

    # print ("taskset:", taskset)
    total_util = get_total_util(taskset)
    if is_harmonic_periods(periods):
        return (1.0 - total_util)

    no_tasks = len(taskset)
    bound = no_tasks * (pow(2, 1.0 / no_tasks) - 1)
    # print("Done")
    print ("util, ", total_util)
    print ("obj: ", (bound - total_util))
    return (bound - total_util)

glob_budgets =[]

def total_util(periods):
    global glob_budgets
    sum = 0
    for i in range(len(periods)):
        if(periods[i] < 0):
            return -1
        sum += float(glob_budgets[i])/float(periods[i])
    return (100 * sum)

def rev_util_constraint(periods, budgets):
    return (-util_constraint(periods, budgets))

def sample_sums(periods):
    print (periods, sum(periods))
    return sum(periods)

def solve_scipy(budgets, e2e_delay_threshold):
    global glob_budgets
    no_tasks = len(budgets)

    # An initial guess of periods
    periods_init = [int(b * 5) for b in budgets]
    # print (budgets)
    print (periods_init, 2 * sum(periods_init))

    bounds = Bounds ([b + 1 for b in budgets], [b * 99 for b in budgets])

    bounds = [(b * 3, b * 100) for b in budgets]
    # print (bounds)

    # con1 = {'type': 'ineq', 'fun': e2e_constraint, 'args': [e2e_delay_threshold]}
    # con2 = {'type': 'ineq', 'fun': util_constraint, 'args': [budgets]}
    glob_budgets = budgets
    coefs = [2 for x in budgets]
    con1 = LinearConstraint(coefs, [0], [e2e_delay_threshold])
    con2 = NonlinearConstraint(total_util, 0, 72)
    cons = [con1, con2]

    sol = minimize_ipopt()

    return sol

def main():
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 10

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    schedulable = 0

    setfile_string = "../dataset_" + str(total_util)

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

        solution = solve_scipy(budgets, e2e_delay_threshold)

        if solution.success:
            print (solution.x, "e2e: ", solution.fun, end_to_end_delay_durr_periods(solution.x), (2 * sum(solution.x)))
            schedulable += 1

        done_tasksets += 1
        print ("Schedulable: {}/{}".format(schedulable, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - schedulable), done_tasksets))

    print ("Schedulable: {}/{}".format(schedulable, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

if __name__ == "__main__":
    main()
