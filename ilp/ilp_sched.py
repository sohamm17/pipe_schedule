import task_generator as task_gen
from ortools.sat.python import cp_model
from utility import *
import os, pickle

def create_model(budgets, e2e_delay_threshold):
    no_tasks = len(budgets)

    m = cp_model.CpModel()

    periods = []
    divisions = []
    # division equality is rounded towards zero.
    # So this adds an offset 1 to the previous variable
    divisions_adjusted = []
    for i in range(no_tasks):
        periods.append(m.NewIntVar(budgets[i], budgets[i] * 100, 'periods' + str(i)))

        divisions.append(m.NewIntVar(0, 99, 'utils' + str(i)))
        divisions_adjusted.append(m.NewIntVar(1, 100, 'utils' + str(i)))

        m.AddDivisionEquality(divisions[i], budgets[i] * 100, periods[i])

        # adjusted because the previous division rounds towards zero
        m.Add(divisions_adjusted[i] == divisions[i] + 1)

    m.Add(sum([divisions_adjusted[i] for i in range(no_tasks)]) <= rms_bound(no_tasks))

    m.Add(sum([periods[i] for i in range(no_tasks)]) <= e2e_delay_threshold)

    return m, periods

def main():
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.85

    e2e_delay_factor = 1

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    schedulable = 0

    setfile_string = "../percent_" + str(total_util)

    if not os.path.isfile(setfile_string):
        with open(setfile_string, "wb") as setfile:
            pickle.dump(current_sets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            current_sets = pickle.load(setfile)

    for single_set in current_sets:
        budgets = [x[0] for x in single_set]
        periods_random = [x[1] for x in single_set]

        e2e_delay_threshold = sum(periods_random) * e2e_delay_factor

        M, periods = create_model(budgets, e2e_delay_threshold)
        solver = cp_model.CpSolver()
        status = solver.Solve(M)
        print ("Solution: {}".format(status))
        if status == cp_model.OPTIMAL:
            print ("Optimal solution found. E2E Delay: {}.".format(solver.ObjectiveValue()))
            schedulable += 1
        elif status == cp_model.FEASIBLE:
            print ("Feasible solution found.")
            schedulable += 1
        elif status == cp_model.INFEASIBLE:
            print ("Infeasible Solution.")
        elif status == cp_model.MODEL_INVALID:
            print ("Invalid Model.")

        # if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        #     for i in range(len(budgets)):
        #         print ("Periods {}: {}".format(i, solver.Value(periods[i])))
        #
        #     taskset = []
        #     for i in range(len(budgets)):
        #         taskset.append((budgets[i], solver.Value(periods[i])))
        #     print ("Total utilization: {}".format(get_total_util(taskset)))

    print ("Schedulable: {}/{}".format(schedulable, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

if __name__ == "__main__":
    main()
