import task_generator as task_gen
from ortools.sat.python import cp_model
from utility import *

def optimize_schedule():
    return None

def create_model(budgets):
    no_tasks = len(budgets)

    m = cp_model.CpModel()

    periods = []
    divisions = []
    for i in range(no_tasks):
        periods.append(m.NewIntVar(budgets[i], budgets[i] * 100, 'periods' + str(i)))

        divisions.append(m.NewIntVar(budgets[i], budgets[i] * 100, 'periods' + str(i)))

    m.AddDivisionEquality()
    m.Add(sum(budgets[i] * (1 // periods[i]) for i in range(no_tasks)) <= rms_bound(no_tasks))

    m.minimize(sum(periods[i] for i in range(no_tasks)))

    return m

def main():
    budgets = [1, 1000]
    M = create_model(budgets)
    solver = M.CpSolver()
    status = solver.Solve(M)
    if status == cp_model.OPTIMAL:
        print ("Optimal solution found. E2E Delay: {}.".format(solver.ObjectiveValue()))


if __name__ == "__main__":
    main()
