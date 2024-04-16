import gurobipy as gp
from gurobipy import GRB
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/supragyabajpai/SchulichJourney_PredectiveModeling/main/non_profits.csv')

# Extract alpha_i and beta_i values
alpha_values = df['alpha_i'].tolist()
beta_values = df['beta_i'].tolist()

# Formulate the Optimization Model
model = gp.Model("Nonprofit_Optimization")

# Decision variables
num_nonprofits = len(alpha_values)
allocations = model.addVars(num_nonprofits, lb=0, vtype=GRB.CONTINUOUS, name="allocations")
effort_terms = model.addVars(num_nonprofits, name="effort_terms")

# Objective function
model.setObjective(gp.quicksum(2 * effort_terms[i] for i in range(num_nonprofits)), GRB.MAXIMIZE)

# Budget constraint
budget_constraint = model.addConstr(gp.quicksum(allocations[i] for i in range(num_nonprofits)) <= 50000000, "Budget")

# Power constraint using addGenConstrPow()
for i in range(num_nonprofits):
    model.addGenConstrPow(allocations[i], effort_terms[i], 2.0/3.0, f"PowConstraint_{i}")

# Optimize the model
model.optimize()

# Analyze the Results
# (a) Effort level e*_i for each nonprofit can be obtained from the allocation
for i in range(num_nonprofits):
    allocation = allocations[i].x
    optimal_effort = (beta_values[i] * allocation) ** 0.33
    print(f"Nonprofit {i+1}: Optimal Effort = {optimal_effort}")

# (b) Total output value
if model.Status == GRB.OPTIMAL:
    print("Optimal solution found.")
    # Print the decision variables
    for v in model.getVars():
        print(f"{v.varName} = {v.x}")
    print(f"Objective Value: {model.ObjVal}")

# (c) Allocation of budget
#budget_allocation = budget_constraint.getAttr(GRB.Attr.Pi)
#print("Allocation of Budget:", budget_allocation)

# (d) Nonprofits receiving no funding
nonfunded_nonprofits = sum(1 for i in range(num_nonprofits) if allocations[i].x == 0)
print("Nonprofits receiving no funding:", nonfunded_nonprofits)