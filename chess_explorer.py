import panel as pn
from api import API
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from helper_functions import *
import matplotlib.pyplot as plt
import hvplot.pandas
import plotly.express as px

# initial database: https://www.kaggle.com/datasets/datasnaek/chess/data

pn.extension()

api = API()
api.load_df("games_clean.csv")

# Search Widgets

# x column of graph/plot
x_column = pn.widgets.Select(name="X Column", options=api.get_columns(), value='rating_diff')

# y column of graph/plot
y_column = pn.widgets.Select(name="Y Column", options=api.get_columns(), value='white_rating')

# whether to consider rated/unrated games only
rated = pn.widgets.Select(name="Rated/Unrated Games", options=['all', 'rated', 'unrated'],
                          value='all')

# width/height of plots
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1000)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)

# CALLBACK FUNCTIONS
def get_catalog(x_column, y_column, rated):
    """
    :param x_column: name of x column gotten from widget
    :param y_column: name of y column gotten from widget
    :param rated: one of ['all', 'rated', 'unrated'] that determines whether to consider rated/unrated games only
    :return: dataframe with x_column and y_column
        depending on value of "rated" will include rated/unrated/all games
    """
    if x_column == y_column:
        return('column names cannot be the same') # if column names are the same, it errors out
    global local
    local = api.extract_two_var_df(x_column, y_column, rated)  # calling the api

    # creates Tabulator widget from df with the 2 input columns, and rated column if it is not included
    table = pn.widgets.Tabulator(local, selectable=False)
    return table

def get_full_df():
    """
    calls extract_full_df(), displays whole dataframe
    """
    global local
    local = api.extract_full_df()
    table = pn.widgets.Tabulator(local, selectable=False)
    return table

def get_plot(x_column, y_column, rated, width, height):
    """
    :param x_column: name of x column gotten from widget
    :param y_column: name of y column gotten from widget
    :param rated: one of ['all', 'rated', 'unrated'] that determines whether to consider rated/unrated games only
    :param width: width of graph gotten from widget
    :param height: height of graph gotten from widget
    :return: graph depending on datatypes of the columns that x_column and y_column correspond to
        if both are numeric, scatter plot
        if x is categorical and y is numeric, multiple boxplots
        if x is numeric and y is categorical, sideways boxplots
            (I could not find another graph with a numeric x axis and categorical y axis)
        if both are categorical, sankey
    """
    if x_column == y_column: # will error out if this is not handled
        return('column names cannot be the same')

    global local
    local = api.extract_two_var_df(x_column, y_column, rated)  # calling the api

    datatypes = api.column_datatypes()
    x_dtype, y_dtype = datatypes[x_column], datatypes[y_column]

    if '64' in str(x_dtype) and '64' in str(y_dtype):
        # EXTRAORDINARILY hacky way to determine if both datatypes are numeric
        plot = px.scatter(local, x_column, y_column, color='rated', height=height, width=width)
        return plot
    elif '64' in str(y_dtype):
        # y variable is numeric, x variable is categorical
        plot = px.box(local, x=x_column, y=y_column, height=height, width=width)
        return plot
    elif '64' in str(x_dtype):
        # x variable is numeric, y variable is categorical
        plot = px.box(local, x=x_column, y=y_column, orientation='h', height=height, width=width)
        return plot
    else:
        # both variables are categorical
        values = [1] * len(local[x_column]) # create values column for sankey
        local['vals'] = values # add to dataframe

        # run helper function to create sankey
        # each pair of values will be assigned a value of 1
        # aggregate_columns will be called within create_sankey to combine values
        # if the src and targ columns have the same value
        fig = create_sankey(local, x_column, y_column, vals='vals', width=width, height=height)
        return fig


# CALLBACK BINDINGS (Connecting widgets to callback functions)
two_var_catalog = pn.bind(get_catalog, x_column, y_column, rated)
plot = pn.bind(get_plot, x_column, y_column, rated, width, height)

# just assigning a variable to get_full_df()
# binding not needed since it does not have any inputs
full_catalog = get_full_df()

# DASHBOARD WIDGET CONTAINERS ("CARDS")
card_width = 320 # value chosen for my own device, mileage may vary

search_card = pn.Card(
    pn.Column(
        x_column,
        y_column,
        rated
    ),
    title="Search", width=card_width, collapsed=False
)

plot_card = pn.Card(
    pn.Column(
        width,
        height
    ),

    title="Plot", width=card_width, collapsed=True
)

layout = pn.template.FastListTemplate(
    title="Chess Explorer",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Two Variable Table", two_var_catalog),
            ('Graph', plot),
            ('Full Table', full_catalog),
            active=1
        )

    ],
    header_background='#a93226'

).servable()

layout.show()

