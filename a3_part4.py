"""CSC110 Fall 2020 Assignment 3, Part 4: Modeling an Epidemic

Instructions (READ THIS FIRST!)
===============================
Implement each of the functions in this file. As usual, do not change any function headers
or preconditions. You do NOT need to add doctests.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 David Liu and Mario Badr.
"""
import csv
import datetime
from typing import Dict, List

import plotly.graph_objects as go
from plotly.subplots import make_subplots


###############################################################################
# Question 1
###############################################################################
def sir_model(n: int, i0: int, beta: float, gamma: float, num_days: int) -> Dict[str, List[int]]:
    """Return the values of S, I, and R in the SIR model for the given parameters.

    Parameter descriptions:
        - n represents the total population number
        - i0 represents I(0), the initial number of infected people
        - beta and gamma are the model parameters (as described in the assignment handout)
        - num_days is the number of days to run the model for
          (time goes from 0 to num_days - 1, inclusive)

    The returned dictionary contains three keys: 'S', 'I', and 'R', representing each
    group in the SIR model.
    The corresponding value of each key is a list of length num_days, where the element
    at index t equals the number of people in that group after t days.
    The element at index 0 is the initial value.

    Preconditions:
        - n > 0
        - 0 < i0 <= n
        - beta >= 0.0
        - 0.0 <= gamma <= 1.0
        - num_days >= 1
    """
    sir_so_far = {'S': [n - i0], 'I': [i0], 'R': [0]}

    for day in range(0, num_days):
        next_s = sir_so_far['S'][day] - min(beta * sir_so_far['I'][day] * (sir_so_far['S'][day]) / n,
                                            sir_so_far['S'][day])
        sir_so_far['S'].append(int(next_S))

        next_I = sir_so_far['I'][day] + min(beta * sir_so_far['I'][day] * (sir_so_far['S'][day]) / n,
                                            sir_so_far['S'][day]) - gamma * sir_so_far['I'][day]
        sir_so_far['I'].append(int(next_I))

        next_R = n - (int(next_S) + int(next_I))
        sir_so_far['R'].append(next_R)

    return sir_so_far


def plot_sir_model(n: int, i0: int, beta: float, gamma: float, num_days: int) -> None:
    """Plot a SIR model using plotly's stacked bar charts.

    The parameters are all the same as for the sir_model function.

    Note that the bars are listed in bottom-up order: Recovered, Infectious, Susceptible.
    We've provided most of the code for you; your task is to fill in the calls
    to go.Bar to provide the proper x and y lists of values.

    See https://plotly.com/python/bar-charts/#stacked-bar-chart.

    Preconditions:
        - n > 0
        - 0 < i0 <= n
        - beta >= 0.0
        - 0.0 <= gamma <= 1.0
        - num_days >= 1
    """
    data = sir_model(n, i0, beta, gamma, num_days)
    days = [x for x in range(0, num_days)]
    # You need to pass in lists for x and y here to create each go.Bar object.
    # The "y" values should come from the data variable above; the "x" values
    # should be a list [0, 1, ..., num_days - 1].
    fig = go.Figure(data=[
        go.Bar(name='Recovered', x=days, y=data['R']),
        go.Bar(name='Infectious', x=days, y=data['I']),
        go.Bar(name='Susceptible', x=days, y=data['S'])
    ])

    title = f'SIR model: N = {n}, I(0) = {i0}, beta = {beta}, gamma = {gamma}'
    fig.update_layout(barmode='stack',
                      title=title,
                      xaxis_title='Days',
                      yaxis_title='Population')
    fig.show()


###############################################################################
# Question 2
###############################################################################
def sird_model(n: int, i0: int, beta: float,
               gamma: float, mu: float, num_days: int) -> Dict[str, List[int]]:
    """Return the values of S, I, R, and D in the SIRD model for the given parameters.

    Parameter descriptions:
        - n represents the total population number
        - i0 represents I(0), the initial number of infected people
        - beta, gamma, and mu are the model parameters (as described in the assignment handout)
        - num_days is the number of days to run the model for
          (time goes from 0 to num_days - 1, inclusive)

    The returned dictionary contains four keys: 'S', 'I', 'R', and 'D'.
    The corresponding value of each key is a list of length num_days, where the element
    at index t equals the number of people in that group after t days.
    The element at index 0 is the initial value.

    Preconditions:
        - n > 0
        - 0 < i0 <= n
        - beta >= 0.0
        - 0.0 <= gamma + mu <= 1.0
        - num_days >= 1

    HINT: this function is VERY similar to sir_model.
    """
    sir_so_far = {'S': [n - i0], 'I': [i0], 'R': [0], 'D': [0]}
    living = n

    for day in range(0, num_days):
        living = sir_so_far['S'][day] + sir_so_far['I'][day] + sir_so_far['R'][day]
        next_S = sir_so_far['S'][day] - min(beta * sir_so_far['I'][day] * (sir_so_far['S'][day]) / living,
                                            sir_so_far['S'][day])
        sir_so_far['S'].append(int(next_S))

        next_I = sir_so_far['I'][day] + min(beta * sir_so_far['I'][day] * (sir_so_far['S'][day]) / living,
                                            sir_so_far['S'][day]) - gamma * sir_so_far['I'][day] - mu * \
                 sir_so_far['I'][day]
        sir_so_far['I'].append(int(next_I))

        next_R = sir_so_far['R'][day] + gamma * sir_so_far['I'][day]
        sir_so_far['R'].append(int(next_R))

        next_D = sir_so_far['D'][day] + living - int(next_S) - int(next_I) - int(next_R)
        sir_so_far['D'].append(next_D)

    return sir_so_far


def plot_sird_model(n: int, i0: int, beta: float, gamma: float, mu: float, num_days: int) -> None:
    """Plot a SIRD model using plotly's stacked bar charts.

    The parameters are all the same as for the sird_model function.

    Include the bars in this order, from the bottom-up: Deaths, Recovered, Infectious, Susceptible.
    You should use the code from plot_sir_model as a starting point. Make sure to update the
    graph title to say "SIRD" rather than "SIR", and show the value of the new parameter "mu".

    Preconditions:
        - n > 0
        - 0 < i0 <= n
        - beta >= 0.0
        - 0.0 <= gamma + mu <= 1.0
        - num_days >= 1
    """
    data = sird_model(n, i0, beta, gamma, mu, num_days)
    days = [x for x in range(0, num_days)]
    # You need to pass in lists for x and y here to create each go.Bar object.
    # The "y" values should come from the data variable above; the "x" values
    # should be a list [0, 1, ..., num_days - 1].
    fig = go.Figure(data=[
        go.Bar(name='Dead', x=days, y=data['D']),
        go.Bar(name='Recovered', x=days, y=data['R']),
        go.Bar(name='Infectious', x=days, y=data['I']),
        go.Bar(name='Susceptible', x=days, y=data['S'])
    ])

    title = f'SIR model: N = {n}, I(0) = {i0}, beta = {beta}, gamma = {gamma}, mu = {mu}'
    fig.update_layout(barmode='stack',
                      title=title,
                      xaxis_title='Days',
                      yaxis_title='Population')
    fig.show()


###############################################################################
# Question 3
###############################################################################
# Source: https://www.ontario.ca/page/ontario-demographic-quarterly-highlights-first-quarter-2020
ONTARIO_POPULATION = 14745040


def read_csv_data(filepath: str, n: int) -> Dict[str, List[int]]:
    """Return a SIRD dictionary from the data mapped from a CSV file.

    n represents the initial population number.

    Preconditions:
        - filepath refers to a csv file in the format of
          data/modeling/ontario_covid_cases_2020_10_17.csv
          (i.e., could be that file or a different file in the same format)
        - n is the size of the population represented in the given csv file
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        data_so_far = {'S': [], 'I': [], 'R': [], 'D': []}
        for row in reader:
            # row is a list of strings
            # Your task is to extract the relevant data from row and add it
            # to the accumulator.
            n = n - (int(row[2]) + int(row[1]) + int(row[3]))
            data_so_far['D'].append(int(row[2]))
            data_so_far['R'].append(int(row[1]))
            data_so_far['I'].append(int(row[3]))
            data_so_far['S'].append(n)

    return data_so_far


def plot_csv_data(filepath: str, n: int, start_date: datetime.date) -> None:
    """Plot the SIRD data from the given filepath using plotly's stacked bar charts.

    The first two parameters are the same as for the read_csv_data function.
    start_date is used as the initial date on the x-axis for this plot. (Unlike
    the first two plotting functions, we want you to label the x-axis with specific
    dates. You can base this on the provided plot_parameter_estimates function below.)

    Note: the first date in the provided Ontario spreadsheet is March 2, 2020.

    Include the bars in this order, from the bottom-up: Deaths, Recovered, Infectious.
    Do NOT show the "Susceptible" bar here.

    We've left this function mostly blank, but you should use the code from plot_sir_model
    as a starting point.

    Preconditions:
        - filepath refers to a csv file in the format of
          data/modeling/ontario_covid_cases_2020_10_17.csv
          (i.e., could be that file or a different file in the same format)
        - n is the size of the population represented in the given csv file
    """

    data = read_csv_data(filepath, n)
    days = [start_date + datetime.timedelta(days=i) for i in range(0, len(data['I']))]
    # You need to pass in lists for x and y here to create each go.Bar object.
    # The "y" values should come from the data variable above; the "x" values
    # should be a list [0, 1, ..., num_days - 1].
    fig = go.Figure(data=[
        go.Bar(name='Dead', x=days, y=data['D']),
        go.Bar(name='Recovered', x=days, y=data['R']),
        go.Bar(name='Infectious', x=days, y=data['I']),
    ])

    title = f'SIR model For Covid-19: N = {n}, '
    fig.update_layout(barmode='stack',
                      title=title,
                      xaxis_title='Days',
                      yaxis_title='Population')
    fig.show()


###############################################################################
# Question 4
###############################################################################
def estimate_parameters(sird_data: Dict[str, List[int]]) -> Dict[str, List[float]]:
    """Return a mapping of SIRD model parameter estimates from the given sird_data.

    Let num_days be the length of each list in sird_data.

    The returned mapping has three keys: 'beta', 'gamma', and 'mu'.
    Each corresponding value is a list of length num_days - 1, whose element at index t
    is an estimate for a parameter (beta/gamma/mu) based on the change in data between
    day t and day (t + 1).

    For example, the element at index 0 in the 'gamma' list is the estimate for parameter
    gamma based on the values of sird_data['R'][0], sird_data['R'][1], and sird_data['I'][0].

    See handout and question 4(a) for given formulas for computing the parameter estimates.

    Preconditions:
        - sird_data has the form returned by sird_model/read_csv_data
    """
    byu_so_far = {'beta': [], 'gamma': [], 'mu': []}
    num_days = len(sird_data['D'])
    for day in range(0, num_days - 1):
        nt = (sird_data['S'][day] + sird_data['I'][day] + sird_data['R'][day])
        tod_beta = \
            -((sird_data['S'][day + 1] - sird_data['S'][day]) / (sird_data['I'][day] * (sird_data['S'][day] / nt)))
        byu_so_far['beta'].append(tod_beta)

        tod_gamma = (sird_data['R'][day + 1] - sird_data['R'][day]) / sird_data['I'][day]
        byu_so_far['gamma'].append(tod_gamma)

        tod_mu = (sird_data['D'][day + 1] - sird_data['D'][day]) / sird_data['I'][day]
        byu_so_far['mu'].append(tod_mu)
    print(byu_so_far)
    return byu_so_far


def plot_estimates(sird_data: Dict[str, List[int]], start_date: datetime.date) -> None:
    """Plot SIRD model parameter estimates based on sird_data using plotly.

    start_date is used as the initial date on the x-axis for this plot.
    Note: the first date in the provided Ontario spreadsheet is March 2, 2020.

    The function is provided for you to visualize your work; you can run/modify this
    function as you see fit.

    Preconditions:
        - sird_data has the form returned by sird_model/read_csv_data
    """
    estimates = estimate_parameters(sird_data)
    days = [start_date + datetime.timedelta(days=i) for i in range(0, len(estimates['beta']))]

    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(go.Scatter(x=days, y=estimates['beta'],
                             mode='lines+markers',
                             name='beta'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=days, y=estimates['gamma'],
                             mode='lines+markers',
                             name='gamma'),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=days, y=estimates['mu'],
                             mode='lines+markers',
                             name='mu'),
                  row=3, col=1)
    fig.update_layout(title='SIRD Model Parameter Estimates', xaxis_title='Date')
    fig.show()


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['read_csv_data'],
        'extra-imports': ['python_ta.contracts', 'csv', 'datetime',
                          'plotly.graph_objects', 'plotly.subplots'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        'disable': ['R1705'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
