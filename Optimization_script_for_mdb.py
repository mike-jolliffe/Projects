#Import linear programming, plotting, and dataframe manipulation functionality
from pulp import *
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from IPython.display import Image

#Get user definition of program constraints
kcal_obligation = int(raw_input("Please choose a kcal target: "))
cost_cap = int(raw_input("Please choose a cost cap: "))
mileage_floor = int(raw_input("Please enter a mileage goal: "))
print "Running Optimization program..."

XL = pd.ExcelFile('Medford_Optimize.xlsx')
data = XL.parse('Sheet1')

# create the LP object, set up as a minimization problem --> since we want to minimize the costs
prob = pulp.LpProblem('MedfordOptimize', pulp.LpMinimize)

#Create decision variables:
decision_variables = []
for rownum, row in data.iterrows():
    variable = str('x' + str(rownum))
    variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat = 'Integer')
    decision_variables.append(variable)

#Define Objective Function
total_cost = ""
for rownum, row in data.iterrows():
    for i,j in enumerate(decision_variables):
        if rownum == i:
            formula = row['Site Cost']*j
            total_cost += formula
prob += total_cost

#Define constraints

kcal_implement = ""
for rownum, row in data.iterrows():
    for i, j in enumerate(decision_variables):
        if rownum == i:
            formula = row['kcals']*j
            kcal_implement += formula
prob += (kcal_implement >= kcal_obligation)

cost_implement = ""
for rownum, row in data.iterrows():
    for i, j in enumerate(decision_variables):
        if rownum == i:
            formula = row['Site Cost']*j
            cost_implement += formula
prob += (cost_implement <= cost_cap)

mileage_implement = ""
for rownum, row in data.iterrows():
    for i, j in enumerate(decision_variables):
        if rownum == i:
            formula = row['mileage']*j
            mileage_implement += formula
prob += (mileage_implement >= mileage_floor)

#Final format of problem
prob.writeLP("MedfordOptimize.lp")

optimization_result = prob.solve()

#assert optimization_result == pulp.LpStatusOptimal
print("Status: ", LpStatus[prob.status])
print("Optimal Solution to the problem: ", value(prob.objective))
print("Individual decision_variables: ")
for v in prob.variables():
    print(v.name, "=", v.varValue)

#Append back to the data set:
variable_name = []
variable_value = []
for v in prob.variables():
    variable_name.append(v.name)
    variable_value.append(v.varValue)

df = pd.DataFrame({'variable': variable_name, 'value': variable_value})
for rownum, row in df.iterrows():
    value = re.findall(r'(\d+)', row['variable'])
    df.loc[rownum, 'variable'] = int(value[0])

df = df.sort_values(by='variable')

#append results
for rownum, row in data.iterrows():
    for results_rownum, results_row in df.iterrows():
        if rownum == results_row['variable']:
            data.loc[rownum, 'decision'] = results_row['value']

#Sites to implement:
print data[data['decision'] == 1]
output = data[data['decision'] == 1]

#How many program acres, miles, kcals, cost:
print "TOTAL ACRES: " + str(data[data['decision'] == 1]['acreage'].sum())

print "TOTAL MILES: " + str(data[data['decision'] == 1]['mileage'].sum())

print "TOTAL KCALS: " + str(data[data['decision'] == 1]['kcals'].sum())

print "TOTAL COST: " + str(data[data['decision'] == 1]['Site Cost'].sum())

#Write to excel
writer = pd.ExcelWriter('Medford_Optimize.xlsx')

data.to_excel(writer,'Sheet1')
output.to_excel(writer,'Recommended sites')
writer.save()
