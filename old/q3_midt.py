import pandas as pd
from gurobipy import *

# Load nurse data from GitHub
nurse_df = pd.read_csv("https://raw.githubusercontent.com/supragyabajpai/SchulichJourney_PredectiveModeling/main/nurse_shift_costs.csv")

# Extracting data from DataFrame
cost_data = nurse_df.set_index('Nurse_ID').to_dict(orient='index')

# Extracting cost dictionaries
weekday_costs = {nurse_id: data['Cost_Weekday'] for nurse_id, data in cost_data.items()}
weekend_costs = {nurse_id: data['Cost_Weekend'] for nurse_id, data in cost_data.items()}
overtime_costs = {nurse_id: data['Cost_Overtime'] for nurse_id, data in cost_data.items()}

# Extracting nurse IDs and categories
nurse_ids = list(cost_data.keys())
categories = [cost_data[nurse_id]['Category'] for nurse_id in nurse_ids]

# Create the optimization model
model = Model("Nurse_Scheduling")

# Define binary variables
shifts_per_week = 14
shifts = [(n, j) for n in nurse_ids for j in range(1, shifts_per_week + 1)]
shift_vars = model.addVars(shifts, vtype=GRB.BINARY, name="shift")

# Define objective function
model.setObjective(
    quicksum(weekday_costs[n] * shift_vars[(n, j)] for n, j in shifts if j % 2 != 0) +
    quicksum(weekend_costs[n] * shift_vars[(n, j)] for n, j in shifts if j % 2 == 0) +
    quicksum(overtime_costs[n] * shift_vars[(n, j)] for n, j in shifts if j % 2 != 0 and n > 6),
    GRB.MINIMIZE)

# Constraints
for j in range(1, shifts_per_week + 1):
    model.addConstr(quicksum(shift_vars[(n, j)] for n in nurse_ids) >= 6, f"At_least_6_nurses_{j}")
    if j % 2 != 0:
        model.addConstr(quicksum(shift_vars[(n, j)] for n in nurse_ids if categories[nurse_ids.index(n)] == 'SRN') >= 1, f"At_least_one_SRN_{j}")
    for n in nurse_ids:
        model.addConstr(quicksum(shift_vars[(n, k)] for k in range(max(1, j - 1), min(shifts_per_week + 1, j + 2))) <= 1,
                        f"No_back_to_back_shifts_{n}_{j}")

# Solve the problem
model.optimize()

# Output results
print("Optimal Objective Function Value (Minimum Cost):", model.objVal)
print("Solution:")
for n, j in shifts:
    if shift_vars[(n, j)].x == 1:
        print(f"Nurse {n} works shift {j}")

# Number of overtime shifts
overtime_shifts = sum(1 for n, j in shifts if j % 2 != 0 and n > 6 and shift_vars[(n, j)].x == 1)
print("Number of overtime shifts:", overtime_shifts)