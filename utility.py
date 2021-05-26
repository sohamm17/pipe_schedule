import numpy as np

"""
returns total utilization of a task set
"""
def get_total_util(task_set):
    return np.sum([float(x[0]) / x[1] for x in task_set])

def get_total_util_2(budgets, periods):
    sum = 0
    for i in range(len(periods)):
        sum += float(budgets[i]) / periods[i]
    print ("utilprint ", sum)
    return sum

"""
returns the end-to-end delay of a pipeline
"""
def end_to_end_delay(pipeline):
    return sum([x[1] for x in pipeline])

"""
Durr et al.[2019] - End-to-end delay upper bound, response-time replaced by
period
"""
def end_to_end_delay_durr(pipeline):
    e2e_ub = 0
    N = len(pipeline)
    for i in range(0, N - 1):
        # If next task is of lower priority (higher or equal period), then P = 0
        P = (0 if pipeline[i + 1][1] >= pipeline[i][1] else 1)
        e2e_ub += max(pipeline[i][1], pipeline[i + 1][1] + pipeline[i][1] * P)
        # print (i, e2e_ub)
    # add the period of first and last tasks
    return (e2e_ub + pipeline[0][1] + pipeline[N - 1][1])


def end_to_end_delay_durr_periods_gekko(periods):
    e2e_ub = 0
    N = len(periods)
    print ("called", periods)
    for i in range(0, N - 1):
        # If next task is of lower priority (higher or equal period), then P = 0
        if periods[i + 1].value >= periods[i].value:
            e2e_ub += periods[i + 1].value
        else:
            e2e_ub += periods[i + 1].value + periods[i].value
        # print (i, e2e_ub)
    # add the period of first and last tasks
    # print (periods, "E2E: ", int(e2e_ub + periods[0] + periods[N - 1]))
    return int(e2e_ub + periods[0].value + periods[N - 1].value)

# Only periods are provided
def end_to_end_delay_durr_periods(periods, m):
    N = len(periods)
    e2e_ub = periods[0] + periods[N - 1]
    # print ("called2", periods)
    for i in range(0, N - 1):
        # If next task is of lower priority (higher or equal period), then P = 0
        e2e_ub += m.if3(periods[i + 1] - periods[i], periods[i + 1] + periods[i], periods[i + 1])
        # print (i, e2e_ub)
    # add the period of first and last tasks
    # print (periods, "E2E: ", int(e2e_ub + periods[0] + periods[N - 1]))
    # print ("c2", e2e_ub + periods[0] + periods[N - 1])
    return e2e_ub

def end_to_end_delay_durr_periods_orig(periods):
    e2e_ub = 0
    N = len(periods)
    for i in range(0, N - 1):
        # If next task is of lower priority (higher or equal period), then P = 0
        if periods[i + 1] >= periods[i]:
            e2e_ub += periods[i + 1]
        else:
            e2e_ub += periods[i + 1] + periods[i]
        # print (i, e2e_ub)
    # add the period of first and last tasks
    # print (periods, "E2E: ", int(e2e_ub + periods[0] + periods[N - 1]))
    return e2e_ub + periods[0] + periods[N - 1]

def end_to_end_delay_durr_periods_pyomo(periods, extra_periods):
    N = len(periods)
    e2e_ub = periods[0] + periods[N - 1]
    for i in range(0, N - 1):
        # If next task is of lower priority (higher or equal period), then P = 0
        e2e_ub += periods[i + 1] + extra_periods[i]
        # print (i, e2e_ub)
    # add the period of first and last tasks
    # print (periods, "E2E: ", int(e2e_ub + periods[0] + periods[N - 1]))
    return e2e_ub

"""
returns RMS bound limit for a value of N
"""
def rms_bound(n):
  return int(100 * n * (pow(2, 1.0 / n) - 1))

"""
Checks if periods are harmonic
"""
def is_harmonic_periods(periods):
    smallest_period = min(periods)

    for p in periods:
        for x in periods:
            smaller = min(p, x)
            greater = max(p, x)
            if greater % smaller != 0:
                # print (p, x)
                return False
    return True

def utilization_bound_gekko(tasks, m, periods):
    total_util = get_total_util (tasks)

    no_tasks = len(tasks)
    bound = no_tasks * (pow(2, 1.0 / no_tasks) - 1)
    # print (1 - total_util)
    return (bound - total_util)

def utilization_bound_test_non_harmo(tasks):
    total_util = get_total_util(tasks)

    no_tasks = len(tasks)
    bound = no_tasks * (pow(2, 1.0 / no_tasks) - 1)
    return total_util <= bound

"""
This is utilization bound test for RMS
"""
def utilization_bound_test(tasks):
    total_util = get_total_util(tasks)
    periods = [x[1] for x in tasks]
    # if is_harmonic_periods(periods):
    #     return (total_util <= 1.0)

    no_tasks = len(tasks)
    bound = no_tasks * (pow(2, 1.0 / no_tasks) - 1)
    return total_util <= 0.69

"""
This function makes taskset harmonic
"""
def make_taskset_harmonic(taskset):
    periods = [x[1] for x in taskset]
    budgets = [x[0] for x in taskset]
    smallest_period = min(periods)
    # print (smallest_period)
    i = 0
    new_taskset = []
    for p in periods:
        if p % smallest_period != 0:
            k = p // smallest_period
            periods[i] = k * smallest_period
        new_taskset.append((budgets[i], periods[i]))
        i += 1

    return new_taskset
