import numpy as np

"""
returns total utilization of a task set
"""
def get_total_util(task_set):
    return np.sum([float(x[0]) / x[1] for x in task_set])

"""
This is a special total utilization function for GEKKO
where we do not apply any float to python
"""
def get_total_util_gekko(task_set):
    return np.sum([x[0] / x[1] for x in task_set])

def get_total_util_2(budgets, periods):
    sum = 0
    for i in range(len(periods)):
        sum += float(budgets[i]) / periods[i]
    print ("utilprint ", sum)
    return sum

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
    total_util = get_total_util_gekko (tasks)

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
    # periods = [x[1] for x in tasks]
    # if is_harmonic_periods(periods):
    #     return (total_util <= 1.0)

    no_tasks = len(tasks)
    bound = no_tasks * (pow(2, 1.0 / no_tasks) - 1)
    return total_util <= bound

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
