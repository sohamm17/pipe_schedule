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

    prios = [] # For the calculation of relative priority among tasks

    e2e_delay = []

    for i in range(no_tasks):
        e2e_delay.append(m.NewIntVar(0, e2e_delay_threshold, "e2e_delay" + str(i)))

        periods.append(m.NewIntVar(budgets[i] + 1, budgets[i] * 100, 'periods' + str(i)))

        divisions.append(m.NewIntVar(1, 100000, 'utils' + str(i)))

        prios.append(m.NewBoolVar('pri' + str(i)))

        m.AddDivisionEquality(divisions[i], budgets[i] * 1000000, periods[i])
        # adjusted because the previous division rounds towards zero
        # m.Add(divisions_adjusted[i] == divisions[i] + 1)

        # start adding from 1 to last task for the previous task
        if i > 0:
            # if next period is small, then next is higher priorty;
            m.Add(periods[i] < periods[i - 1]).OnlyEnforceIf(prios[i - 1])
            m.Add(periods[i] >= periods[i - 1]).OnlyEnforceIf(prios[i - 1].Not())

            m.Add(e2e_delay[i] == e2e_delay[i - 1] + periods[i] + periods[i - 1]).OnlyEnforceIf(prios[i - 1])
            m.Add(e2e_delay[i] == e2e_delay[i - 1] +  periods[i]).OnlyEnforceIf(prios[i - 1].Not())
            # m.AddImplication(periods[i] < periods[i - 1], prios[i - 1])
            # m.AddImplication(periods[i] >= periods[i - 1], prios[i - 1].Not())
            # m.AddImplication(prios[i - 1].Not(), e2e_delay[i] == periods[i])
            # m.AddImplication(prios[i - 1], e2e_delay[i] == periods[i] + periods[i - 1])
        else:
            m.Add(e2e_delay[i] == periods[i])

    # total_util = m.NewIntVar(10, 717734, "total")
    total_util = m.NewIntVar(10, 15000000, "total")

    m.Add(total_util == sum(divisions))
    m.Minimize(e2e_delay[no_tasks - 1] + periods[no_tasks - 1])
    m.Add(total_util <= 0.718)

    return m, periods, divisions

def main():
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 14

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    schedulable = 0

    setfile_string = "../dataset_" + str(total_util) + "_" + str(no_tasks)

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

        M, periods, divisions = create_model(budgets, e2e_delay_threshold)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 5.0
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

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for i in range(len(budgets)):
                print ("Task ({}, {}) -- {}".format(budgets[i], solver.Value(periods[i]), solver.Value(divisions[i])))

            taskset = []
            for i in range(len(budgets)):
                taskset.append((budgets[i], solver.Value(periods[i])))
            print ("Total utilization: {}, E2E_UB: {}".format(get_total_util(taskset), end_to_end_delay_durr(taskset)))

        done_tasksets += 1
        print ("Schedulable: {}/{}".format(schedulable, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - schedulable), done_tasksets))

    print ("Schedulable: {}/{}".format(schedulable, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

if __name__ == "__main__":
    main()
