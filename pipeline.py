import numpy as np


def sample_rate_lb_helper(budgets, periods):
    fx = 1 # Sampling Rate
    N = len(budgets)
    if N == 1:
        return 1
    elif N == 2:
        return float(periods[0])/periods[1]
    else:
        prev_pipeline_fx = sample_rate_lb_helper(budgets[:N - 1], periods[:N - 1])

        second_last_period = periods[N - 2]
        last_period = periods[N - 1]
        is_oversample = True if last_period <= second_last_period else False

        if (prev_pipeline_fx < 1 and is_oversample): # Case 1
            return prev_pipeline_fx
        elif prev_pipeline_fx < 1 and not is_oversample: # Case 2
            return prev_pipeline_fx * (float(second_last_period) / last_period)
        elif prev_pipeline_fx >= 1 and is_oversample: # Case 3
            return prev_pipeline_fx * (float(second_last_period) / last_period)
        else: # Case 4
            return (1 / prev_pipeline_fx) * (float(second_last_period) / last_period)

"""
The following function calculates sampling rate LB of an asynchronous
pipeline.
"""
def sample_rate_lb(pipeline):
    budgets = [t[0] for t in pipeline]
    periods = [t[1] for t in pipeline]
    return sample_rate_lb_helper(budgets, periods)

"""
The following function calculates loss rate UB of an asynchronous
pipeline.
"""
def loss_rate_ub(pipeline):
    if sample_rate_lb(pipeline) <= 1:
        return  (1 - sample_rate_lb(pipeline))
    else:
        return 0

"""
This calculates the minimum throughput of a Pipeline
"""
def throughput_lb_helper(budgets, periods, initial_budgets):
    return min((float(budgets[i]) / initial_budgets[i]) for i in range(len(periods)))

def throughput_lb(pipeline, initial_budgets):
    budgets = [t[0] for t in pipeline]
    periods = [t[1] for t in pipeline]
    return throughput_lb_helper(budgets, periods, initial_budgets)
