from ast import And
from ntpath import join
import pandas as pd
import csv

def main(sorting_function):
    with open('large.csv') as csv_file:
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
    jobs = pd.read_csv('large.csv', skiprows=[0,1], header=None)
    sorted_data = sorting_function(jobs)
    current_cpu_usage = 0
    current_memory_usage = 0
    selected_jobs =  pd.DataFrame(columns=['selected_order','job_id','cpu_demand','memory_demand','payment','sorting_criterion'])
    total_cost = 0
    j = 0
    for i, job in sorted_data.iterrows():
        new_cpu_usage = current_cpu_usage + job[1]
        new_memory_usage = current_memory_usage + job[2]
        if new_cpu_usage > int(max_cpu_capacity) or new_memory_usage > int(max_memory_capacity) :
            break
        current_cpu_usage = new_cpu_usage
        current_memory_usage = new_memory_usage
        total_cost += job[3]
        selected_jobs.loc[j] = [int(j),job[0],job[1],job[2],job[3],job['sorting_criterion']]
        j += 1

    print("\nThe selected jobs are:")
    print(selected_jobs)
    print("\nMax CPU and memory usage allowed:")
    print(max_cpu_capacity, max_memory_capacity)
    print("\nThe CPU and Memory used are:\n")
    print(current_cpu_usage, current_memory_usage)
    print(f"\n The total revenue earned: {total_cost}\n")
    
#sorting based on cost to resource ratio
def sort_based_on_cost_to_resource_heuristic(data: pd.DataFrame):
    print("\nSorting by cost to cpu & memory ratio")
    cost_to_resource_ratios = []
    for _, job in data.iterrows():
        cost_to_cst = job[3] / (job[1]+ job[2])
        cost_to_resource_ratios.append(cost_to_cst)
    data['sorting_criterion'] = cost_to_resource_ratios
    return data.sort_values(by='sorting_criterion', ascending= False)

#sorting based on highest cost
def sort_based_on_higher_cost_heuristic(data: pd.DataFrame):
    print("\nSorting by cost alone")
    data['sorting_criterion'] = data[data.columns[3]]
    return data.sort_values(by=data.columns[3], ascending= False)

main(sort_based_on_higher_cost_heuristic)
print("\n=========================\n")
main(sort_based_on_cost_to_resource_heuristic)
