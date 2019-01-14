from pulp import *
import pandas as pd
import matplotlib.pyplot as plt


def blend(ingredients, costs, variables, requirements):
    """
    takes ingredients, costs, and amounts of variables
    plots a pie chart of the optimal blend - minimising cost
    :param ingredients:     list of ingredient names
    :param costs:            dict of names and costs
    :param variables:       dict of dict
                              key: name of variable
                              value: dict
                                  key: name of ingredient
                                  value: percent of variable in ingredient
    :param requirements:    dict:
                                key: name of variable
                                value: minimum amount required
    :return: pie chart output of blend amounts
    """

    prob = LpProblem("General Blend Problem", LpMinimize)
    ingredient_vars = LpVariable.dicts("Ingr", ingredients, 0)
    prob += lpSum([costs[i] * ingredient_vars[i] for i in ingredients]), "Total Cost of Ingredients per can"
    prob += lpSum([ingredient_vars[i] for i in ingredients]) == 100, "Percentages sum"
    for req in requirements:
        prob += lpSum([variables[req][i] * ingredient_vars[i] for i in ingredients]) >= requirements[req], req
    prob.writeLP("GeneralBlend.lp")
    prob.solve()
    print("Status: ", LpStatus[prob.status])

    pie_data = []
    pie_labels = []
    for v in prob.variables():
        pie_data += [v.varValue]
        pie_labels += [v.name]
        print(v.name, '=', v.varValue)

    print("Total cost of ingredients per can =", value(prob.objective))
    pieData = pd.Series(pie_data)
    pieData.plot(kind='pie', labels=pie_labels)
    plt.show()

    return prob

if __name__ == "__main__":
    pass
