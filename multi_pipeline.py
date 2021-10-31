#!/usr/bin/python

"""
This program tries to schedule multiple Pipelines in Multicore with
partitioned RMS scheduling.
"""
import numpy as np
import optimized_sched as sched
from pipeline import *
import os, sys, getopt, pickle, random
from utility import *
import copy

num_cores = 4

#Available Utilizations in each core
core_avl_util = [(0, 0.69), (1, 0.69), (2, 0.69), (3, 0.69), (4, 0.69), (5, 0.69), (6, 0.69), (7, 0.69)]

tasks_in_cores = []

running_pipelines = []

number_of_migrations = 0
number_of_unsuccess_migrations = 0

# For 10 tasks Pipelines
MIN_E2E_FACTOR = 6
MAX_E2E_FACTOR = 8

MIN_LOSS_FACTOR = 50
MAX_LOSS_FACTOR = 80

MIGRATION = True
ONLINE_ADJUSTMENT = True

# Initialize global variables
def init():
    global core_avl_util, tasks_in_cores, number_of_migrations, number_of_migrations
    core_avl_util = [(0, 0.69), (1, 0.69), (2, 0.69), (3, 0.69), (4, 0.69), (5, 0.69), (6, 0.69), (7, 0.69)]
    tasks_in_cores = []
    running_pipelines = []
    number_of_migrations = 0
    number_of_migrations = 0

def set_cores (number_of_cores):
    global num_cores, core_avl_util, tasks_in_cores
    num_cores = number_of_cores
    core_avl_util = core_avl_util[:num_cores]
    for i in range(number_of_cores):
        tasks_in_cores.append([])

def set_e2e_factor(no_tasks):
    global MIN_E2E_FACTOR, MAX_E2E_FACTOR
    # 1.7-1.8 for 5 tasks. 1.7-2.1 for 3 tasks.
    MIN_E2E_FACTOR = 1.7
    MAX_E2E_FACTOR = 1.8
    print ("MIN_E2E_FACTOR, MAX_E2E_FACTOR: ", MIN_E2E_FACTOR, MAX_E2E_FACTOR)

def get_core_avl_util(core_no):
    for core in core_avl_util:
         if core[0] == core_no:
             return core[1]

def set_core_avl_util(core_no, util):
    i = 0
    for i in range(len(core_avl_util)):
        if core_avl_util[i][0] == core_no:
            core_avl_util[i] = (core_avl_util[i][0], util)
            break

def get_total_available_utilization():
    i = 0
    utilsum = 0
    for i in range(len(core_avl_util)):
        utilsum += get_core_avl_util(i)
    return utilsum

def core_utilization(core_no):
    utilsum = 0
    for task in tasks_in_cores[core_no]:
        utilsum += task_util(task)
    return utilsum

def total_core_utilization():
    utilsum = 0
    for core in tasks_in_cores:
        for task in core:
            utilsum += task_util(task)
    return utilsum

def get_separate_core_utils():
    arr = []
    for i in range(num_cores):
        arr.append(core_utilization(i))
    return arr

# unmap task from core
def unmap_task_from_core(core_no, task):
    i = 0
    for t in tasks_in_cores[core_no]:
        if t['id'] == task['id']:
            del tasks_in_cores[core_no][i]
            set_core_avl_util(core_no, get_core_avl_util(core_no) + task_util(task))
            break
        i += 1

# remove pipeline from cores
# qualified pipelines are given
def remove_pipeline(q_pipeline):
    for a_task in q_pipeline['tasks']:
        unmap_task_from_core(a_task['core'], a_task)
    i = 0
    for p in running_pipelines:
        if p['PIPELINE_ID'] == q_pipeline['PIPELINE_ID']:
            del running_pipelines[i]
            break
        i += 1


def core_assign_to_task(task, core_no):
    task['core'] = core_no

def map_task_to_core(core_no, task):
    set_core_avl_util(core_no, get_core_avl_util(core_no) - task_util(task))
    # print ("Mapped task ", task['id'], " in core ", core_no, ". Rest util in core: ", get_core_avl_util(core_no))

    # task to core in core_structures
    tasks_in_cores[core_no].append(task)

    # task to core in task structures
    core_assign_to_task(task, core_no)

def migrate_tasks(needed_util, pipeline):
    local_core_avl_util = copy.deepcopy(core_avl_util)
    local_core_avl_util = sorted(local_core_avl_util, key=lambda x: x[1], reverse=True)
    i = 0

    accum_util = 0
    for i in range(len(local_core_avl_util)):
        cur_core_no = local_core_avl_util[i][0]
        tasks_this_core_decreasing = sorted(tasks_in_cores[cur_core_no], key=lambda t: t['budget'] /t['period'], reverse=True)
        for this_task in tasks_this_core_decreasing:
            for c in core_avl_util:
                # If not the current core and there is some space in other core, move the task there
                if c[0] == cur_core_no:
                    continue
                if task_util(this_task) <= get_core_avl_util(c[0]):
                    # print ("Migrating task", this_task['id'], "from", this_task['core'], "to", c[0])
                    # print (tasks_in_cores[c[0]])
                    # print (tasks_in_cores[cur_core_no])
                    map_task_to_core(c[0], this_task)
                    unmap_task_from_core(cur_core_no, this_task)
                    # print (tasks_in_cores[c[0]])
                    # print (tasks_in_cores[cur_core_no])
                    return
                    # print (local_core_avl_util, get_total_available_utilization())
                    # sys.exit(1)

# pipeline of tasks
def WFD_FIT(pipeline):
    global core_avl_util, num_cores, number_of_migrations, number_of_unsuccess_migrations
    # Sort the tasks by utilization
    sorted_tasklist = sorted(pipeline['tasks'], key=lambda t: t['budget'] /t['period'], reverse=True)
    # And now map as First-fit

    # Try migrating at least the number of core times
    migrations = 0
    while migrations < num_cores:
        mapped = 0

        # To get a task to core mapping
        local_core_avl_util = copy.deepcopy(core_avl_util)
        task_to_core_map = []

        for task in sorted_tasklist:
            local_core_avl_util = sorted(local_core_avl_util, key=lambda x: x[1], reverse=True)
            for i in range(len(local_core_avl_util)):
                if task_util(task) <= local_core_avl_util[i][1]:
                    local_core_avl_util[i] = (local_core_avl_util[i][0], local_core_avl_util[i][1] - task_util(task))
                    task_to_core_map.append(local_core_avl_util[i][0])
                    mapped += 1
                    break

        # We have a valid mapping
        if mapped == len(pipeline['tasks']):
            i = 0
            for task in sorted_tasklist:
                map_task_to_core(task_to_core_map[i], task)
                i += 1
            number_of_migrations += migrations
            return True
        elif MIGRATION:
            migrate_tasks(None, None)
            migrations += 1
        else:
            return False
    number_of_unsuccess_migrations += migrations
    return False

# pipeline of tasks
def FFD_FIT(pipeline):
    global core_avl_util
    # Sort the tasks by utilization
    sorted_tasklist = sorted(pipeline, key=lambda t: t['budget'] / t['period'], reverse=True)
    print (sorted_tasklist)
    # And now map as First-fit
    mapped = 0

    # To get a task to core mapping
    local_core_avl_util = copy.deepcopy(core_avl_util)
    task_to_core_map = []

    for task in sorted_tasklist:
        for i in range(len(local_core_avl_util)):
            if task_util(task) <= local_core_avl_util[i]:
                local_core_avl_util[i] -= task_util(task)
                task_to_core_map.append(i)
                mapped += 1
                break

    # We have a valid mapping
    if mapped == len(pipeline):
        i = 0
        for task in sorted_tasklist:
            map_task_to_core(task_to_core_map[i], task)
            i += 1
        return True
    else:
        return False

# Start from the first producer and
# Start from the last consumer and keep dividing budgets and periods
# Until initial budget - Basically continue the third stage further
# Then start from first producer:
# increase periods of the producers
# current period <= next consumer's period
# and Loss Rate <= Upper Bound
# and E2E <= Upper Bound
def reduce_pipeline_util(pipeline):
    return True

ID = 0
PIPELINE_ID = 0
def pipeline_with_init_budgets(pipeline, init_budget, e2e_ub=0, lr_ub=0):
    global ID, PIPELINE_ID
    new_pipeline = []
    for i in range(len(pipeline)):
        new_pipeline.append({'id': ID, 'budget': pipeline[i][0], 'period': pipeline[i][1], 'init_budget': init_budget[i], 'e2e_ub': e2e_ub, 'lr_ub': lr_ub})
        ID += 1
    the_pipeline = {'PIPELINE_ID': PIPELINE_ID, 'tasks': new_pipeline}
    PIPELINE_ID += 1
    return the_pipeline

def get_period_budget_tupled_pipeline(pipeline):
    return [(t['budget'], t['period']) for t in pipeline]

def get_budgets(pipeline):
    return [t['budget'] for t in pipeline]

def get_init_budgets(pipeline):
    return [t['init_budget'] for t in pipeline]

def adjust_existing_pipeline(heur_reject=True, start=0):
    global running_pipelines
    if heur_reject:
        # This means that we do not have enough utilization that the heuristics could give us a feasible schedule
        # So optimize exisitng Pipelines
        for pipeline in running_pipelines[start:]:
            # print ("Running Pipeline ", pipeline)
            cur_util = get_total_util(get_period_budget_tupled_pipeline(pipeline['tasks']))
            e2e_ub = pipeline['tasks'][0]['e2e_ub']
            lr_ub = pipeline['tasks'][0]['lr_ub']
            new_taskset, opti = sched.optimize_alpha_live(get_budgets(pipeline['tasks']), e2e_ub, lr_ub, cur_util - 0.05, starting_alpha = 2)
            if new_taskset is not None:
                # print (new_taskset, opti, get_total_util(new_taskset), cur_util)
                saved_pipeline = copy.deepcopy(pipeline)
                remove_pipeline(pipeline)
                returned_pipeline = pipeline_with_init_budgets(new_taskset, get_init_budgets(saved_pipeline['tasks']), e2e_ub, lr_ub)
                running_pipelines.append(returned_pipeline)
                return WFD_FIT(returned_pipeline)
                # sys.exit(1)
            # return True
    return False


def get_average(the_list):
    return float(sum(the_list)) / len(the_list)

def main(argv):
    global num_cores, core_avl_util, tasks_in_cores, running_pipelines, number_of_migrations, number_of_unsuccess_migrations, ONLINE_ADJUSTMENT
    try:
        opts, args = getopt.getopt(argv, "p:t:r:c:")
    except getopt.GetoptError:
        print ('python multi_pipeline.py -p <number of pipelines> -t <number of tasks in each Pipeline> -c <number of processors> -r <number of runs>')
        sys.exit(2)

    no_tasks = 0
    no_pipelines = 0
    runs = 0
    number_of_cores = 0
    for opt, arg in opts:
        if opt == '-p':
            no_pipelines = int(arg)
        elif opt == '-t':
            no_tasks = int(arg)
        elif opt == '-r':
            runs = int(arg)
        elif opt == '-c':
            number_of_cores = int(arg)

    mapper_rejections = []
    heuristic_rejections = []
    mapped_pipelines_all_runs = []
    optimized23_pipelines = [] # Stage2/3 Optimized Pipelines
    used_core_utils = []
    total_migrations = []
    total_unsuccess_migrations = []

    for run_id in range(runs):
        print ("RUN ID -----------------------", run_id)
        init()
        ID = 0 # TASK ID
        PIPELINE_ID = 0

        SEED = 50 * run_id
        random.seed(SEED)
        set_cores(number_of_cores)
        set_e2e_factor(no_tasks)

        pipeline_budgets = GetPipelineBudgets(no_pipelines, no_tasks, SEED)

        mapped_pipelines = 0
        reject_heuristic = 0
        optimized = 0 # Optimized by our Stage2/3 heuristics
        for pipeline in pipeline_budgets:
            e2e_ub = int(sum(pipeline) * no_tasks * (float(random.randint(MIN_E2E_FACTOR * 100, MAX_E2E_FACTOR * 100)) / 100))
            loss_rate = random.randint(MIN_LOSS_FACTOR, MAX_LOSS_FACTOR) / 100
            # print (e2e_ub, loss_rate)

            existing_pipeline_adj = 0
            while existing_pipeline_adj < 1:
                # print("First Total Avl Util: ", get_total_available_utilization())
                suggest_util = get_total_available_utilization() # min(get_total_available_utilization(), 0.69)

                taskset, opti = sched.optimize_alpha_live(pipeline, e2e_ub, loss_rate, suggest_util, starting_alpha=2)

                if opti is not None and opti > 1:
                    optimized += 1

                if taskset is None and ONLINE_ADJUSTMENT:
                    # print ("Pipeline is rejected by heuristic. Avl: ", get_total_available_utilization())
                    existing_pipeline_adj += 1
                    # print ("Trying Pipeline Adjustments")
                    if adjust_existing_pipeline(True, start=existing_pipeline_adj-1):
                        print ("Success in Adjustment")
                        # print ("Now: ", get_total_available_utilization())
                        continue
                    # else:
                    #     print ("Could not adjust an existing Pipeline")
                else:
                    break

            if taskset is not None:
                current_pipeline = pipeline_with_init_budgets(taskset, pipeline, e2e_ub, loss_rate)
                # print (get_total_util(taskset))
                if WFD_FIT(current_pipeline):
                    running_pipelines.append(current_pipeline)
                    mapped_pipelines += 1
                    # print ("Pipeline Mapped.")
                    # print (tasks_in_cores)
                # else:
                #     print ("Pipeline rejected by mapper.")
            else:
                reject_heuristic += 1

        print ("Mapped Pipelines: {}/{}".format(mapped_pipelines, no_pipelines))
        print ("Rejected by Heuristic: {}/{}".format(reject_heuristic, no_pipelines))
        print ("Rejected by Mapper: {}/{}".format(no_pipelines - reject_heuristic - mapped_pipelines, no_pipelines))
        print ("Optimized by Stage 2-3:", optimized)

        mapped_pipelines_all_runs.append(mapped_pipelines)
        heuristic_rejections.append(reject_heuristic)
        mapper_rejections.append(no_pipelines - reject_heuristic - mapped_pipelines)
        optimized23_pipelines.append(optimized)
        used_core_utils.append(total_core_utilization())
        total_migrations.append(number_of_migrations)
        total_unsuccess_migrations.append(number_of_unsuccess_migrations)

    print ("total runs", runs, "-- mapped pipelines, heuristic rejections, mapper rejections, optimized2/3 stage, used core utilization:")
    print (get_average(mapped_pipelines_all_runs), get_average(heuristic_rejections), get_average(mapper_rejections), get_average(optimized23_pipelines), get_average(used_core_utils), get_average(total_migrations), get_average(total_unsuccess_migrations))

    return True

if __name__ == "__main__":
    main(sys.argv[1:])
