#%%
#-------PART F--------#
import gurobipy as gp
from gurobipy import GRB

# Define scenario data
scenarios = range(1, 17)
probabilities = [0.09, 0.12, 0.10, 0.05, 0.16, 0.14, 0.03, 0.08, 
                 0.05, 0.05, 0.04, 0.03, 0.02, 0.01, 0.02, 0.01]
gallons_used = [90, 95, 100, 105, 110, 115, 120, 125, 130, 
                135, 140, 145, 150, 155, 160, 165]

# Create model
model = gp.Model("Stochastic_Programming")

# Define decision variables
order_advance = model.addVar(vtype=GRB.CONTINUOUS, name="order_advance")

# Set objective function
model.setObjective(order_advance * 95, GRB.MINIMIZE)

# Add constraint for expected gallons used
model.addConstr(sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios) <= order_advance, "expected_gallons_constraint")

# Optimize model
model.optimize()

# Retrieve solution
if model.status == GRB.OPTIMAL:
    gallons_ordered = order_advance.x
    total_cost = model.objVal
    print(f"Optimal gallons of coffee to order in advance: {gallons_ordered}")
    print(f"Optimal objective function value (total cost): {total_cost}")
else:
    print("No solution found")


#------------------PART G-----------------------#
#%%
# Define scenario data
scenarios = range(1, 17)
probabilities = [0.09, 0.12, 0.10, 0.05, 0.16, 0.14, 0.03, 0.08, 
                 0.05, 0.05, 0.04, 0.03, 0.02, 0.01, 0.02, 0.01]
gallons_used = [90, 95, 100, 105, 110, 115, 120, 125, 130, 
                135, 140, 145, 150, 155, 160, 165]

# Define supplier prices
price_advance = 95

# Calculate the total cost of ordering in advance
total_cost_advance = price_advance * sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios)

# Find the optimal quantity of coffee to order in advance
optimal_quantity = sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios)

# Calculate the cost per gallon at the optimal quantity
cost_per_gallon_optimal = total_cost_advance / optimal_quantity

# Round the result to the nearest dime
cost_per_gallon_optimal_rounded = round(cost_per_gallon_optimal, 1)

print(f"At a price per gallon of ${cost_per_gallon_optimal_rounded}, it makes sense for conference organizers not to order any coffee in advance.")

# %%

# Calculate the expected value of using the solution from the mean value problem (EEV)
eev = sum(gallons_used) * price_advance

# Calculate the value of the stochastic solution (VSS)
vss = total_cost_advance - eev

print(f"Expected Value of using the Solution from the Mean Value Problem (EEV): ${eev}")
print(f"Value of the Stochastic Solution (VSS): ${vss}")

#%%
# Define scenario data
scenarios = range(1, 17)
probabilities = [0.09, 0.12, 0.10, 0.05, 0.16, 0.14, 0.03, 0.08, 
                 0.05, 0.05, 0.04, 0.03, 0.02, 0.01, 0.02, 0.01]
gallons_used = [90, 95, 100, 105, 110, 115, 120, 125, 130, 
                135, 140, 145, 150, 155, 160, 165]

# Define supplier prices
price_advance = 95

# Calculate the total cost of ordering in advance
total_cost_advance = price_advance * sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios)

# Find the optimal quantity of coffee to order in advance
optimal_quantity = sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios)

# Calculate the cost per gallon at the optimal quantity
cost_per_gallon_optimal = total_cost_advance / optimal_quantity

# Round the result to the nearest dime
cost_per_gallon_optimal_rounded = round(cost_per_gallon_optimal, 1)

print(f"At a price per gallon of ${cost_per_gallon_optimal_rounded}, it makes sense for conference organizers not to order any coffee in advance.")

#%%
# Define scenario data
scenarios = range(1, 17)
probabilities = [0.09, 0.12, 0.10, 0.05, 0.16, 0.14, 0.03, 0.08, 
                 0.05, 0.05, 0.04, 0.03, 0.02, 0.01, 0.02, 0.01]
gallons_used = [90, 95, 100, 105, 110, 115, 120, 125, 130, 
                135, 140, 145, 150, 155, 160, 165]

# Define supplier prices
price_advance = 95

# Calculate the maximum possible amount of coffee to order in advance
max_quantity = max(probabilities[n-1] * gallons_used[n-1] for n in scenarios)

# Calculate the total cost of ordering the maximum possible amount in advance
total_cost_max_quantity = price_advance * max_quantity

# Calculate the cost per gallon at the maximum quantity
cost_per_gallon_max_quantity = total_cost_max_quantity / max_quantity

# Round the result to the nearest dime
cost_per_gallon_max_quantity_rounded = round(cost_per_gallon_max_quantity, 1)

print(f"At a price per gallon of ${cost_per_gallon_max_quantity_rounded}, it makes sense for conference organizers to order the maximum possible amount of coffee in advance.")

#%%

# Define scenario data
scenarios = range(1, 17)
probabilities = [0.09, 0.12, 0.10, 0.05, 0.16, 0.14, 0.03, 0.08, 
                 0.05, 0.05, 0.04, 0.03, 0.02, 0.01, 0.02, 0.01]
gallons_used = [90, 95, 100, 105, 110, 115, 120, 125, 130, 
                135, 140, 145, 150, 155, 160, 165]

# Define supplier prices
price_advance = 95

# Calculate the total cost of ordering in advance
total_cost_advance = price_advance * sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios)

# Calculate the total cost under WS (perfect foresight)
total_cost_ws = sum(probabilities[n-1] * gallons_used[n-1] for n in scenarios) * price_advance

# Calculate the expected value of perfect information (EVPI)
evpi = max(total_cost_ws - total_cost_advance, 0)

print(f"Expected Value of Perfect Foresight (WS): ${total_cost_ws}")
print(f"Expected Value of Perfect Information (EVPI): ${evpi}")


#%%

# Calculate the expected value of using the solution from the mean value problem (EEV)
eev = sum(gallons_used) * price_advance

# Calculate the value of the stochastic solution (VSS)
vss = total_cost_advance - eev

print(f"Expected Value of using the Solution from the Mean Value Problem (EEV): ${eev}")
print(f"Value of the Stochastic Solution (VSS): ${vss}")


# %%
