import numpy as np

"""
returns total utilization of a task set
"""
def get_total_util(task_set):
    return np.sum([float(x[0]) / x[1] for x in task_set])

"""
returns the end-to-end delay of a pipeline
"""
def end_to_end_delay(pipeline):
    return sum([x[1] for x in pipeline])

"""
This is utilization bound test for RMS
"""
def utilization_bound_test(tasks):
  no_tasks = len(tasks)
  total_util = get_total_util(tasks)
  bound = no_tasks * (pow(2, 1.0 / no_tasks) - 1)
  if total_util <= bound:
    return True
  else:
    return False
