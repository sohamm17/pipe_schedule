import task_generator as task_gen
from utility import *
import os, pickle, sys
import numpy as np
from pipeline import *

from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition
from pyomo.gdp import *

def e2e_constraint(periods, threshold):
    print ("periods ", periods)
    print ("e2e", end_to_end_delay_durr_periods(periods))
    diff = (threshold - end_to_end_delay_durr_periods(periods))
    return (threshold - end_to_end_delay_durr_periods(periods))
    # if diff >= 0:
    #     return (threshold - end_to_end_delay_durr_periods(periods))
    # else:
    #     return -np.Inf

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
    print (taskset)
    return (bound - total_util)

glob_budgets =[]

def total_util(periods):
    global glob_budgets
    sum = 0
    for i in range(len(periods)):
        sum += float(glob_budgets[i])/periods[i].value
    print (periods, sum)
    return (100 * sum)

def rev_util_constraint(periods, budgets):
    return (-util_constraint(periods, budgets))

def greater_eq(p1, p2, prio):
    # set prio of p2 >= p1
    return (p2 - p1 >= p1 * (1 - prio))

def period_sum(model):
    tot = model.periods[0]
    for i in range(1, len(model.periods)):
        tot += model.periods[i]
    # print ("objective:", tot)
    return tot

def period_mult(model):
    tot = 1
    for i in range(1, len(model.periods)):
        tot *= (model.periods[i - 1] / model.periods[i])
    # print ("objective:", tot)
    return tot

def period_bound (model, i):
    return (glob_budgets[i] * 1.5, glob_budgets[i] * 20000)

e2e_thr = 0
def period_init (model, i):
    global e2e_thr
    return int (glob_budgets[i] * 400)

def prio_init(model, i):
    return int(glob_budgets[i + 1] >= glob_budgets[i])

def check_e2e(model):
    return (end_to_end_delay_durr_periods_pyomo(model.periods, model.extra_periods) <= e2e_thr)

def log_con1(model, i):
    return model.dis[4 * i + 1].indicator_var.implies(model.dis[4 * i + 2].indicator_var)

def log_con2(model, i):
    return model.dis[4 * i + 3].indicator_var.implies(model.dis[4 * i + 4].indicator_var)

def greater_rule(model, i):
    N = len(model.periods)
    return model.periods[i] >= model.periods[i - 1] if i < N else Constraint.Skip

under_75 = 0
under_50 = 0
under_25 = 0
under_0  = 0

def solve_pyomo(budgets, e2e_delay_threshold):
    global glob_budgets, under_0, under_25, under_50, under_75
    global e2e_thr
    glob_budgets = budgets
    e2e_thr = e2e_delay_threshold

    no_tasks = len(budgets)

    model = ConcreteModel()

    periods = []
    prios = []

    model.tasks = RangeSet(no_tasks - 1)
    model.double_tasks = RangeSet(2 * (no_tasks - 1))
    model.quadruple_tasks = RangeSet(4 * (no_tasks - 1))

    model.periods = Var(range(0, no_tasks), domain=PositiveIntegers, bounds = period_bound, initialize = period_init)
    # model.extra_periods = Var(range(0, no_tasks - 1), domain=NonNegativeIntegers, bounds = period_bound, initialize = 0)

    # model.dis = Disjunct(model.quadruple_tasks)
    # model.disjns = BooleanVar(model.tasks)
    #
    # for i in range(0, no_tasks - 1):
    #     model.dis[4 * i + 1].Cond = Constraint(expr=model.periods[i + 1] - model.periods[i] >= 0)
    #     model.dis[4 * i + 2].Result = Constraint(expr=model.extra_periods[i] == 0)
    #
    #     # model.dis[2 * i + 1].e2e = Constraint(rule=check_e2e(model))
    #     # model.dis[2 * i + 1].UtilB = Constraint(rule=utilization_bound_test(taskset))
    #
    #     model.dis[4 * i + 3].Cond = Constraint(expr=model.periods[i + 1] + 1 <= model.periods[i])
    #     model.dis[4 * i + 4].Result = Constraint(expr=model.extra_periods[i] == model.periods[i])
    #     # model.dis[2 * i + 2].e2e = Constraint(rule=check_e2e(model))
    #     # model.dis[2 * i + 2].UtilB = Constraint(rule=utilization_bound_test(taskset))
    #
    #     # model.disjns[i + 1] = [model.dis[4 * i + 1], model.dis[4 * i + 3]]
    #
    # model.greatereq = LogicalConstraint(range(0, no_tasks - 1),rule=log_con1)
    # model.smaller = LogicalConstraint(range(0, no_tasks - 1),rule=log_con2)
    # # sys.exit(1)
    #
    # TransformationFactory('core.logical_to_linear').apply_to(model)
    # # TransformationFactory('gdp.bigm').apply_to(model)
    # TransformationFactory('gdp.hull').apply_to(model)
    # model.greatereq.pprint()
    # model.smaller.pprint()
    # model.dis.pprint()

    taskset = []
    for i in range(len(budgets)):
        taskset.append((budgets[i], model.periods[i]))
    model.UtilB = Constraint(rule=utilization_bound_test_non_harmo(taskset))

    # Increasing Period Constraint
    # model.Increasing_P = Constraint(model.tasks, rule=greater_rule)
    # model.Increasing_P.pprint()
    # sys.exit(1)

    # # model.C2 = Constraint(expr=2 * summation(model.periods) <= e2e_delay_threshold)
    # model.E2E_UB = Constraint(rule=check_e2e)

    # model.Util = Objective(expr=get_total_util_2(budgets, model.periods), sense=minimize)
    # model.E2EObj = Objective(expr=end_to_end_delay_durr_periods_pyomo(model.periods, model.extra_periods), sense=minimize)
    # TransformationFactory('gdp.cuttingplane').apply_to(model)
    model.SUM = Objective(rule=period_sum, sense=minimize)
    # model.LR = Objective(rule=period_mult, sense=minimize)

    # model.pprint()

    # print ("Solving")

    results = SolverFactory('ipopt').solve(model, tee=False)
    # results = SolverFactory('glpk').solve(model, tee=False)
    # print (results)
    # model.display()
    # model.pprint()
    final_periods = [int(model.periods[i].value) for i in range(no_tasks)]
    # extra_final_periods = [int(model.extra_periods[i].value) for i in range(no_tasks - 1)]
    # print(budgets, final_periods, extra_final_periods)
    # print(end_to_end_delay_durr_periods_orig(final_periods), e2e_delay_threshold)
    # # print("PY: ", value(model.E2EObj))
    # print(get_total_util_2(budgets, final_periods))
    # print (model.periods[0].value)
    # sys.exit(1)
    # return (None, None)
        # print (results)
    # model.load(results)
    # print ("results;", results)

    # model.display()
    # model.pprint()

    return results, final_periods


def main():
    global under_0, under_25, under_50, under_75
    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75

    e2e_delay_factor = 18

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

        results, periods = solve_pyomo(budgets, e2e_delay_threshold)
        if results != None and (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
            print ("PyomoE2E: ", end_to_end_delay_durr_periods_orig(periods))
            # print (periods, "e2e: ", solution.options.objfcnval, end_to_end_delay_durr_periods_orig(periods), get_total_util_2(budgets, periods))
            final_taskset = [(budgets[i], periods[i]) for i in range(len(budgets))]
            if end_to_end_delay_durr_periods_orig(periods) <= e2e_delay_threshold and get_total_util(final_taskset) <= 0.72:
                print("Also Schedulable")
                # print (budgets, periods)
                schedulable += 1

                lr = loss_rate_ub(final_taskset, budgets)
                if lr <= 0:
                    under_0 += 1
                    # print ("0 Loss Rate:", final_taskset, budgets)
                if lr <= 0.25:
                    under_25 += 1
                if lr <= 0.50:
                    under_50 += 1
                if lr <= 0.75:
                    under_75 += 1

                print ("LR: ", lr)

        done_tasksets += 1
        print ("Schedulable: {}/{}".format(schedulable, done_tasksets))

        print ("Unschedulable: {}/{}".format((done_tasksets - schedulable), done_tasksets))

        print ("under_0, under_25, under_50, under_75: ", under_0, under_25, under_50, under_75)

    print ("Schedulable: {}/{}".format(schedulable, no_tasksets))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

    print ("E2E Factor:", e2e_delay_factor)

if __name__ == "__main__":
    main()
