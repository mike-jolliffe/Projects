from pulp import *
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from IPython.display import Image

kcal_obligation = int(raw_input("Please choose a kcal target: "))
cost_cap = int(raw_input("Please choose a cost cap: "))
print "Running Optimization program..."

XL = pd.ExcelFile('Optimization_1.xlsx')
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
            formula = row['Cost']*j
            total_cost += formula
prob += total_cost

#Define constraints

kcal_implement = ""
for rownum, row in data.iterrows():
    for i, j in enumerate(decision_variables):
        if rownum == i:
            formula = row['Kcals']*j
            kcal_implement += formula

prob += (kcal_implement >= kcal_obligation)

cost_implement = ""
for rownum, row in data.iterrows():
    for i, j in enumerate(decision_variables):
        if rownum == i:
            formula = row['Cost']*j
            cost_implement += formula
prob += (cost_implement <= cost_cap)

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

#How many acres:
print "TOTAL ACRES: " + str(data[data['decision'] == 1]['Acres'].sum())

print "TOTAL KCALS: " + str(data[data['decision'] == 1]['Kcals'].sum())

print "TOTAL COST: " + str(data[data['decision']== 1]['Cost'].sum())

writer = pd.ExcelWriter('Optimization_1.xlsx')

data.to_excel(writer,'Sheet1')
output.to_excel(writer,'Recommended sites')
writer.save()
