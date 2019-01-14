from flask import Flask, render_template, request, redirect
from blending_general import blend

from pulp import *
import pandas as pd
import matplotlib.pyplot as plt
import blend_example_data

# New stuff
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



app = Flask(__name__)

INGREDIENTS_COUNT = 0
VARIABLES_COUNT = 0
VARIABLE_NAMES = []

INGREDIENT_NAMES = []
COSTS = {}
VARIABLES = {}
REQUIREMENTS = {}


@app.route('/example_visualisation')
def example_visualisation():
    prob = blend(blend_example_data.ingredients, blend_example_data.costs, blend_example_data.variables,
                 blend_example_data.requirements)
    status = LpStatus[prob.status]
    cost = value(prob.objective)

    return render_template('show_results.html', status=status, cost=cost)


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



@app.route('/')
def index():
    global INGREDIENTS_COUNT
    INGREDIENTS_COUNT = 0

    global VARIABLES_COUNT
    VARIABLES_COUNT = 0

    global VARIABLE_NAMES
    VARIABLE_NAMES = []

    global INGREDIENT_NAMES
    INGREDIENT_NAMES = []

    global COSTS
    COSTS = {}

    global VARIABLES
    VARIABLES = {}

    global REQUIREMENTS
    REQUIREMENTS = {}

    return render_template('index.html')


@app.route('/get_counts', methods=['POST'])
def get_counts():
    global INGREDIENTS_COUNT
    INGREDIENTS_COUNT = int(request.form['ingredients_count'])

    global VARIABLES_COUNT
    VARIABLES_COUNT = int(request.form['variables_count'])

    return redirect('/enter_ingredient_names')


@app.route('/enter_ingredient_names')
def enter_counts():
    global INGREDIENTS_COUNT
    global VARIABLES_COUNT
    return render_template('enter_ingredient_names.html', ingredients=INGREDIENTS_COUNT, variables=VARIABLES_COUNT)


@app.route('/get_ingredient_names', methods=['POST'])
def collect_ingredient_names():
    global INGREDIENT_NAMES

    for pair in request.form:
        INGREDIENT_NAMES += [request.form[pair]]

    return redirect('/enter_ingredient_costs')


@app.route('/enter_ingredient_costs')
def enter_ingredient_costs():
    global INGREDIENT_NAMES

    return render_template('enter_ingredient_costs.html', ingredients=INGREDIENT_NAMES)


@app.route('/get_costs', methods=['POST'])
def get_costs():
    global COSTS

    for key in request.form:
        COSTS[key] = float(request.form[key])

    return redirect('/enter_variable_names')


@app.route('/enter_variable_names')
def enter_variables():
    return render_template('enter_variable_names.html', variables=VARIABLES_COUNT)


@app.route('/get_variable_names', methods=['POST'])
def get_variable_names():
    global VARIABLE_NAMES

    for key in request.form:
        VARIABLE_NAMES += [request.form[key]]

    return redirect('/enter_variable_amounts')


@app.route('/enter_variable_amounts')
def enter_variable_amounts():
    global VARIABLE_NAMES
    global INGREDIENT_NAMES

    return render_template('enter_variable_amounts.html', ingredients=INGREDIENT_NAMES, variables=VARIABLE_NAMES)


@app.route('/get_variable_amounts', methods=['POST'])
def get_variable_amounts():
    global VARIABLE_NAMES
    global INGREDIENT_NAMES
    global VARIABLES

    for var in VARIABLE_NAMES:
        new_dict = {}
        for ing in INGREDIENT_NAMES:
            new_dict[ing] = float(request.form[var + '_' + ing])
        VARIABLES[var] = new_dict

    return redirect('/enter_requirements')


@app.route('/enter_requirements')
def enter_requirements():
    global VARIABLE_NAMES
    global INGREDIENT_NAMES
    return render_template('enter_requirements.html', variables=VARIABLE_NAMES, ingredients=INGREDIENT_NAMES)


@app.route('/get_requirements', methods=['POST'])
def get_requirements():
    global REQUIREMENTS
    global VARIABLE_NAMES
    for var in VARIABLE_NAMES:
        REQUIREMENTS[var] = float(request.form[var])

    return redirect('/blend')


@app.route('/blend')
def show_solution():
    global INGREDIENT_NAMES
    global COSTS
    global VARIABLES
    global REQUIREMENTS

    print('_' * 10)
    print('ingredient names: ')
    for ing in INGREDIENT_NAMES:
        print('    ' + ing)

    print('_' * 10)
    print('Costs')
    for key in COSTS:
        print('    ' + key + ': ' + str(COSTS[key]))

    print('_' * 10)
    print('Variables: ')
    for key in VARIABLES:
        print('    ' + key + ': ' + str(VARIABLES[key]))

    print('_' * 10)
    print('Requirements: ')
    for key in REQUIREMENTS:
        print('    ' + key + ': ' + str(REQUIREMENTS[key]))

    prob = blend(INGREDIENT_NAMES, COSTS, VARIABLES, REQUIREMENTS)
    status = LpStatus[prob.status]

    # TODO: Show graph on website
    return render_template('show_results.html', status=status)
    return "Doneskies"


if __name__ == '__main__':
    app.run()
