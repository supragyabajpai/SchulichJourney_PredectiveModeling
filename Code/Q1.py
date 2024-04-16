#%%
import pandas as pd
from gurobipy import *

supply_data = pd.read_csv('https://raw.githubusercontent.com/supragyabajpai/SchulichJourney_PredectiveModeling/main/ecogreen_energy_supply.csv')
demand_data = pd.read_csv('https://raw.githubusercontent.com/supragyabajpai/SchulichJourney_PredectiveModeling/main/ecogreen_energy_demand.csv')

provinces = demand_data["Province Index"].tolist()
sites = supply_data.index.tolist()
capacity = supply_data["Capacity"].tolist()
fixed_cost = supply_data["Fixed"].tolist()
variable_cost = supply_data.drop(columns=["Fixed", "Capacity"]).values.tolist()
demand = demand_data["Demand"].tolist()

model = Model("EcoGreen")

plant_open = {(i, j): model.addVar(vtype=GRB.BINARY, name=f"PlantOpen_{i}_{j}") 
              for i in range(1, 21) for j in provinces}
energy_supply = {(i, j): model.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name=f"EnergySupply_{i}_{j}") 
                 for i in range(1, 21) for j in provinces}

model.update()

model.setObjective(quicksum(fixed_cost[i-1] * plant_open[(i, j)] + variable_cost[i-1][j-1] * energy_supply[(i, j)] 
                            for i in range(1, 21) for j in provinces), GRB.MINIMIZE)

for j in provinces:
    model.addConstr(plant_open[(10, j)] + plant_open[(15, j)] + plant_open[(20, j)] <= 1)

for j in provinces:
    model.addConstr(plant_open[(3, j)] <= plant_open[(4, j)] + plant_open[(5, j)])
    model.addConstr(plant_open[(5, j)] <= plant_open[(8, j)] + plant_open[(9, j)])

model.addConstr(quicksum(plant_open[(i, j)] for i in range(1, 11) for j in provinces) 
                <= 2 * quicksum(plant_open[(i, j)] for i in range(11, 21) for j in provinces))

model.addConstr(quicksum(energy_supply[(i, j)] for i in range(1, 6) for j in provinces) 
                >= 0.3 * quicksum(energy_supply[(i, j)] for i in range(1, 21) for j in provinces))

for i in range(1, 21):
    for j in provinces:
        model.addConstr(energy_supply[(i, j)] <= 0.5 * demand[j-1])

for i in range(1, 21):
    for j in provinces:
        model.addConstr(energy_supply[(i, j)] <= capacity[i-1] * plant_open[(i, j)])

for j in provinces:
    model.addConstr(quicksum(energy_supply[(i, j)] for i in range(1, 21)) >= demand[j-1])

model.optimize()

print("Optimized Plan:")
for j in provinces:
    print(f"Province {j}:")
    for i in range(1, 21):
        if plant_open[(i, j)].x > 0.5:
            print(f"\tPlant {i}: Open")
            print(f"\t\tEnergy Supply: {energy_supply[(i, j)].x}")
        else:
            print(f"\tPlant {i}: Closed")
    print()

print('Total Cost: %g' % model.objVal)

province_supply_count = {i: 0 for i in range(1, 21)}

for i in range(1, 21):
    for j in provinces:
        if energy_supply[(i, j)].X > 0.5:
            province_supply_count[i] += 1

for i in range(1, 21):
    print(f"Plant {i} can supply to {province_supply_count[i]} distinct provinces.")

all_variables = model.getVars()

total_vars = len(all_variables)
binary_vars_count = sum(1 for v in all_variables if v.vType == GRB.BINARY)
continuous_vars_count = sum(1 for v in all_variables if v.vType == GRB.CONTINUOUS)

print(f"Total number of variables: {total_vars}")
print(f"Number of binary variables: {binary_vars_count}")
print(f"Number of continuous variables: {continuous_vars_count}")

model.optimize()

if model.status == GRB.OPTIMAL:
    optimal_cost = model.objVal
    print("Optimal Cost:", optimal_cost)
else:
    print("Optimal solution was not found.")

plants_established = 0
num_provinces = 10
num_plants = 20

plant_open = [False] * num_plants

for i in range(1, num_plants + 1):
    for j in range(1, num_provinces + 1):
        if energy_supply[(i, j)].X > 0.5:
            plant_open[i-1] = True
            break

plants_established = sum(1 for is_open in plant_open if is_open)

print(f"Number of power plants established: {plants_established}")

plants_per_province = {j: 0 for j in range(1, 11)}

for i in range(1, 21):
    for j in range(1, 11):
        if energy_supply[(i, j)].X > 0.5:
            plants_per_province[j] += 1

max_plants = max(plants_per_province.values())
min_plants = min(plants_per_province.values())

print(f"Highest number of power plants supplying a single province: {max_plants}")
print(f"Lowest number of power plants supplying a single province: {min_plants}")

model.optimize()

if model.status == GRB.OPTIMAL:
        best_obj = model.objVal
        print("Best Objective:", best_obj)

        model.setParam('PoolSearchMode', 2)
        model.setParam('PoolGap', 0.01)
        model.setParam('PoolSolutions', 200)

        model.optimize()

        num_solutions = model.SolCount
        print(f"Number of solutions found within 1% of the optimal: {num_solutions}")

        for i in range(num_solutions):
            model.setParam('SolutionNumber', i)
            print(f"Solution {i+1} objective value: {model.PoolObjVal}")

else:
    print("Optimal solution was not found.")
