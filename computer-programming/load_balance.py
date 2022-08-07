from ortools.linear_solver import pywraplp
import pandas as pd
import csv

def main():
    with open('small.csv') as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     for row in csv_reader:
        if line_count == 0:
            number_of_jobs = row[0]
        elif line_count == 1:
            max_cpu_capacity = row[0]
            max_memory_capacity = row[1]
        if line_count > 1:
            break
        line_count += 1
    jobs = pd.read_csv('small.csv', skiprows=[0,1], header=None)

    number_of_jobs = len(jobs)
    print(number_of_jobs, jobs.shape)

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
     print('SCIP solver unavailable.')
     return

    x = {}
    for i in range(number_of_jobs):
            x[i] = (solver.BoolVar('x%i' % i))
    cpu_constraints = []
    memory_constraints = []
    objective = solver.Objective()
    for i, job in jobs.iterrows():
        cpu_constraints.append(x[i]*job[1])
        memory_constraints.append(x[i]*job[2])
        objective.SetCoefficient(x[i], int(job[3]))

    # constraints
    print(max_cpu_capacity, max_memory_capacity)
    solver.Add(sum(cpu_constraints) <= int(max_cpu_capacity))
    solver.Add(sum(memory_constraints) <= int(max_memory_capacity))
    # objective
    objective.SetMaximization()
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        cpu_used = 0
        memory_used = 0
        for i, job in jobs.iterrows():
            cpu_used += x[i].solution_value() * job[1]
            memory_used += x[i].solution_value() * job[2]
        print(f'Total cost = {solver.Objective().Value()}\n')
        print(f'Max CPU available = {max_cpu_capacity}, CPU used = {cpu_used}\n')
        print(f'Max Memory available = {max_memory_capacity}, Memory used = {memory_used}\n')
    else:
        print('No solution found.')
    
main()