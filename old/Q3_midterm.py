import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Load nurse data from URL
url = "https://raw.githubusercontent.com/supragyabajpai/SchulichJourney_PredectiveModeling/main/nurse_shift_costs.csv"
nurse_df = pd.read_csv(url)

# Extracting data from DataFrame
nurses = nurse_df['Nurse_ID'].tolist()
categories = nurse_df['Category'].tolist()
weekday_costs = dict(zip(nurses, nurse_df['Cost_Weekday']))
weekend_costs = dict(zip(nurses, nurse_df['Cost_Weekend']))
overtime_costs = dict(zip(nurses, nurse_df['Cost_Overtime']))

# Define the problem
problem = LpProblem("Nurse_Scheduling", LpMinimize)

# Define binary variables
shifts = [(n, j) for n in nurses for j in range(1, 15)]
x = LpVariable.dicts("x", shifts, cat='Binary')

# Define objective function
problem += lpSum([weekday_costs[n] * x[(n, j)] for n, j in shifts if j % 2 != 0]) \
           + lpSum([weekend_costs[n] * x[(n, j)] for n, j in shifts if j % 2 == 0]) \
           + lpSum([overtime_costs[n] * x[(n, j)] for n, j in shifts if j % 2 != 0 and n > 6]), "Total_Cost"

# Constraints
for j in range(1, 15):
    problem += lpSum(x[(n, j)] for n in nurses) >= 6, f"At_least_6_nurses_{j}"
    if j % 2 != 0:
        problem += lpSum(x[(n, j)] for n in nurses if categories[n - 1] == 'SRN') >= 1, f"At_least_one_SRN_{j}"
    for n in nurses:
        problem += lpSum(x[(n, j)] for j in range(max(1, j - 1), min(15, j + 2))) <= 1, f"No_back_to_back_shifts_{n}_{j}"

# Solve the problem
problem.solve()

# Output results
print("Optimal Objective Function Value:", round(problem.objective.value(), 2))
print("Solution:")
for n, j in shifts:
    if x[(n, j)].value() == 1:
        print(f"Nurse {n} works shift {j}")

# Number of overtime shifts
overtime_shifts = sum([x[(n, j)].value() for n, j in shifts if j % 2 != 0 and n > 6])
print("Number of overtime shifts:", int(overtime_shifts))