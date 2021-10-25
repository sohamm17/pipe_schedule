import numpy as np
import os, sys, pickle, random
import task_generator as task_gen

"""
Returns the utilization of a task
"""
def task_util(task):
    return float(task['budget']) / task['period']

# GEKKO = 0
model = None

def sample_rate_lb_helper(budgets, periods, initial_budgets, GEKKO=0):
    fx = 1 # Sampling Rate
    N = len(budgets)
    if N == 1:
        return 1
    elif N == 2:
        budget_multiplier_producer = budgets[0] // initial_budgets[0]
        budget_multiplier_consumer = budgets[1] // initial_budgets[1]
        fx = (1.0 * periods[0]/periods[1]) * (budget_multiplier_consumer / budget_multiplier_producer)
        # print ("L: ", N, fx)
        return fx
    else:
        prev_pipeline_fx = sample_rate_lb_helper(budgets[:N - 1], periods[:N - 1], initial_budgets[:N - 1], GEKKO)

        second_last_period = periods[N - 2]
        last_period = periods[N - 1]

        second_last_budget = budgets[N - 2]
        last_budget = budgets[N - 1]
        second_last_initial_budget = initial_budgets[N - 2]
        last_initial_budget = initial_budgets[N - 1]

        second_last_initial_budget_multipl = second_last_budget // second_last_initial_budget

        last_initial_budget_multipl = last_budget // last_initial_budget

        if GEKKO:
            is_oversample = GEKKO.if3(second_last_period - last_period, 0, 1)
        else:
            is_oversample = True if last_period <= second_last_period else False


        last_sampling_rate = ((1.0 * second_last_period) / last_period) * (last_initial_budget_multipl / second_last_initial_budget_multipl)

        if GEKKO:
            temp = GEKKO.if3(prev_pipeline_fx - 1, 1, 0)
            fx = GEKKO.if3(temp + is_oversample - 2, prev_pipeline_fx * last_sampling_rate, prev_pipeline_fx)
        else:
            if (prev_pipeline_fx < 1 and is_oversample): # Case 1
                fx = prev_pipeline_fx
            else: # Other cases
                fx = prev_pipeline_fx * last_sampling_rate
            # elif prev_pipeline_fx < 1 and not is_oversample: # Case 2
            #     fx = prev_pipeline_fx * last_sampling_rate
            # elif prev_pipeline_fx >= 1 and is_oversample: # Case 3
            #     fx = prev_pipeline_fx * last_sampling_rate
            # else: # Case 4
            #     fx = (1 / prev_pipeline_fx) * last_sampling_rate
        # print ("Loss: ", N, fx)
        return fx

"""
The following function calculates sampling rate LB of an asynchronous
pipeline.
"""
def sample_rate_lb(pipeline, initial_budgets, GEKKO=0):
    budgets = [t[0] for t in pipeline]
    periods = [t[1] for t in pipeline]
    return sample_rate_lb_helper(budgets, periods, initial_budgets, GEKKO)

"""
The following function calculates loss rate UB of an asynchronous
pipeline.
"""
def loss_rate_ub(pipeline, initial_budgets):
    sr = sample_rate_lb(pipeline, initial_budgets)
    if sr >= 1:
        return 0
    else:
        return (1 - sr)

def loss_rate_ub_GEKKO(pipeline, initial_budgets, m):
    model = m
    sr = sample_rate_lb(pipeline, initial_budgets, GEKKO=m)
    lr = model.if3(1 - sr, 0, (1 - sr))
    return lr

"""
This calculates the minimum throughput of a Pipeline
"""
def throughput_lb_helper(budgets, periods, initial_budgets):
    return min((float(budgets[i]) / initial_budgets[i]) for i in range(len(periods)))

def throughput_lb(pipeline, initial_budgets):
    budgets = [t[0] for t in pipeline]
    periods = [t[1] for t in pipeline]
    return throughput_lb_helper(budgets, periods, initial_budgets)


"""
Get existing Pipelines Set
"""
def GetPipelineBudgets(no_pipelines, no_tasks, seed):
    random.seed(seed)

    # MIN_BUDGET = 5
    # MAX_BUDGET = 100
    pipeline_budgets = []

    setfile_string = "pipelines_" + str(no_pipelines) + "_" + str(no_tasks) + "_" + str(seed) + ".pickle"

    if not os.path.isfile(setfile_string):
        min_period = 100
        max_period = 1000

        utils_sets = task_gen.gen_uunifastdiscard(no_pipelines, 0.15, no_tasks)

        period_sets = task_gen.gen_periods_uniform(no_tasks, no_pipelines, min_period, max_period, True)

        current_sets = task_gen.gen_tasksets(utils_sets, period_sets, True)

        for i in range(no_pipelines):
            budgets = []
            for j in range(no_tasks):
                budgets.append(current_sets[i][j][0])
            pipeline_budgets.append(budgets)

        with open(setfile_string, "wb") as setfile:
            pickle.dump(pipeline_budgets, setfile)
    else:
        with open(setfile_string, "rb") as setfile:
            # return None
            pipeline_budgets = pickle.load(setfile)
            # temp = []
            # for i in range(no_pipelines):
            #     budgets = []
            #     for j in range(no_tasks):
            #         budgets.append(pipeline_budgets[i][j][0])
            #     temp.append(budgets)
            # return temp

    return pipeline_budgets
