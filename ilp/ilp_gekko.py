import task_generator as task_gen
from utility import *
from pipeline import *
import os, pickle, sys, getopt
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

"""
budgets: initial budgets
e2e_delay_threshold: E2E Delay Upper Bound
With_Loss: Boolean, whether loss-rate constraint to be applied
Budget_Adj: Boolean, whether to apply the budget adjustment constraint
Loss_UB: If loss-rate is applied, what is the upper bound
"""
def solve_gekko(budgets, e2e_delay_threshold, With_Loss = False, Budget_Adj= False, Loss_UB = 1):
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
    budget_multipliers = []

    for i in range(no_tasks):
        # initial budget * 400 is chosen empirically to be the
        # inital period value for the solver
        # Other values were giving worse result
        periods.append(m.Var(value = (budgets[i] * 400), lb = int(budgets[i] * 1.5), ub = budgets[i] * 20000, integer = True))
        if Budget_Adj:
            budget_multipliers.append(m.Var(value = 1, lb = 1, ub = 100, integer = True))
        # periods.append(m.Var(value = 5, lb = 0, ub = 10, integer = True))
        # Increasing Period Constraint
        # if i > 0:
        #     m.Equation(periods[i] >= periods[i - 1])

    glob_budgets = budgets

    taskset = []
    for i in range(len(budgets)):
        if Budget_Adj:
            taskset.append((budgets[i] * budget_multipliers[i], periods[i]))
        else:
            taskset.append((budgets[i], periods[i]))

    m.Equation(end_to_end_delay_durr_GEKKO(periods, m)<=e2e_delay_threshold)
    m.Equation(utilization_bound_gekko(taskset, m, periods)>= 0.0)

    # m.Obj(end_to_end_delay_durr_GEKKO(periods, m))
    # m.Obj(sum(periods))
    # m.Obj(loss_rate_ub_GEKKO(taskset, budgets, m))
    if With_Loss:
        sr = sample_rate_lb(taskset, budgets, GEKKO=m)
        m.Equation(sr >= 1.0 - Loss_UB)
    try:
        m.solve(disp=False)
        # print("GEKKO ", m.options.objfcnval)
        if With_Loss or Budget_Adj:
            if Budget_Adj:
                final_taskset = [(int(budgets[i] * budget_multipliers[i].value[0]), int(periods[i].value[0])) for i in range(len(budgets))]
            else:
                final_taskset = [(int(budgets[i]), int(periods[i].value[0])) for i in range(len(budgets))]
            # Additional check because the solver might not adhere
            if With_Loss:
                lr = loss_rate_ub(final_taskset, budgets)
                # to every constraint in these cases because of if3/2
                if int(100 * lr) > int(100 * Loss_UB):
                    # print (final_taskset, lr, 1 - sr.value[0], sr.value)
                    # print (budgets)
                    return (None, None)
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

def main(argv):
    Loss_UB = -1
    e2e_delay_factor = -1
    with_loss = False
    budget_adj = False

    usage = 'Usage: python ilp/ilp_gekko.py -w <with loss-rate constraint or not 0/1> -l <loss_rate> -e <LBG> -b <budget adjustment constraint to be added 0/1>\n By default runs without loss-rate constraint'

    try:
        opts, args = getopt.getopt(argv, "w:l:e:b:")
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            Loss_UB = float(arg)
            if Loss_UB > 1:
                print ("loss_rate cannot be more than 1. cannot proceed.")
                print (usage)
                sys.exit(2)
        elif opt == '-e':
            e2e_delay_factor = float(arg)
        elif opt == '-w':
            with_loss = int(arg)
        elif opt == '-b':
            budget_adj = int(arg)

    if Loss_UB == -1 and with_loss:
        print ("Loss Rate UB is not provided.")
        print (usage)
        sys.exit(2)

    if e2e_delay_factor == -1:
        print ("E2E Delay UB in the form of Latency Budget Gap (LBG) is not provided.")
        print (usage)
        sys.exit(2)

    accepted_time_taken = []
    rejected_time_taken = []

    no_tasks = 10
    no_tasksets = 1000

    min_period = 100
    max_period = 1000

    total_util = 0.75 # Just to generate a distribution by UUnifast

    utils_sets = task_gen.gen_uunifastdiscard(no_tasksets, total_util, no_tasks)

    period_sets = task_gen.gen_periods_uniform(no_tasks, no_tasksets, min_period, max_period, True)

    current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

    schedulable = 0

    setfile_string = "./dataset_" + str(total_util) + "_" + str(no_tasks)

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
        solution, periods = solve_gekko(budgets, e2e_delay_threshold, With_Loss=with_loss, Budget_Adj = budget_adj, Loss_UB = Loss_UB)
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

    with open("accepted_sets_gekko.txt", "a") as f:
        f.write("{} ".format(schedulable))

    print ("Unschedulable: {}/{}".format((no_tasksets - schedulable), no_tasksets))

    avg_accept_time = int(1000 * float(sum(accepted_time_taken)) / schedulable)
    print ("Average Accepted Time Taken: ", avg_accept_time, "ms")

    with open("accepted_time_gekko.txt", "a") as f:
        f.write("{} ".format(avg_accept_time))

    if schedulable < no_tasksets:
        avg_failed_time = int(1000 * float(sum(rejected_time_taken)) / (no_tasksets - schedulable))

        print ("Average Rejected Time Taken: ", avg_failed_time, "ms")

        with open("failed_time_gekko.txt", "a") as f:
            f.write("{} ".format(avg_failed_time))

    print ("E2E Factor:", e2e_delay_factor)

    print ("under_0, under_25, under_50, under_75: ", under_0, under_25, under_50, under_75)

if __name__ == "__main__":
    main(sys.argv[1:])
