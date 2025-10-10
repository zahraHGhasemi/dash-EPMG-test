

import pandas as pd
import numpy as np

import dash
from dash import dcc, html, Input, Output

import plotly.express as px
import dash_bootstrap_components as dbc
# from utils.data_loader import load_and_concat_data
# from utils.dataframe_melter import melt_dataframe
# from components.overview import overview_layout
# from components.supply import supply_layout
# from components.power import power_layout
# from components.sector import sector_layout
# from components.search import search_layout
# from components.emissionCO2 import emissionCO2_layout   
from callbacks.overview_callback import register_overview_callbacks
from callbacks.supply_callback import register_supply_callbacks
from callbacks.power_callback import register_power_callbacks
from callbacks.emissionCO2_callback import register_emissionCO2_callback
from callbacks.sector_callback import register_sector_callbacks
from callbacks.subsector_callbacks.subsector_overview_callback import register_subsector_overview_callback
from callbacks.subsector_callbacks.subsector_transport_callback import register_subsector_transport_callback
from callbacks.subsector_callbacks.subsector_residential_callback import register_subsector_residential_callback
from callbacks.subsector_callbacks.subsector_services_callback import register_subsector_services_callback
from callbacks.subsector_callbacks.subsector_industry_callback import register_subsector_industry_callback
from callbacks.search_callback import register_search_callbacks
from callbacks.tab_content_callbacks import register_tab_content_callbacks

from utils.dataframe_melter import get_scenarios, get_data_melted




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)
server = app.server


scenarios = get_scenarios()
# all_data_melted = get_data_melted()
app.title = "Energy Scenarios Dashboard"


app.layout = html.Div([
    html.Div([
        html.Label("Select Scenario:", className="control-label"),
        dcc.Dropdown(
            id='scenario-dropdown',
            options=[{'label': s, 'value': s} for s in scenarios],
            value=scenarios[0] if len(scenarios) > 0 else None,
            placeholder="Select a scenario...",
            className="dropdown"
        )
    ], className="control-item"),
    dcc.RangeSlider(
        id='year-slider',
        min= 2018, #all_data_melted['Year'].min(),
        max= 2050, #all_data_melted['Year'].max()-1,
        value=[2018, 2050],
        marks={str(year): str(year) for year in range( 2018,2050,1)}, #range(all_data_melted['Year'].min(), all_data_melted['Year'].max(), 1)},
        step=1
    ),
    dcc.Tabs(id ='tabs', value = 'overview', children =[
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='Supply', value='supply'),
        dcc.Tab(label='Power', value='power'),
        dcc.Tab(label='Sector', value='sector'),
        dcc.Tab(label='CO2 Emissions', value='co2'),
        dcc.Tab(label='Search', value='search')
        # dcc.Tab(label='Overview', children= overview_layout),
        # dcc.Tab(label ="Supply", children = supply_layout),
        # dcc.Tab(label='Power', children= power_layout),
        # dcc.Tab(label ="Sector" , children= sector_layout),
        # dcc.Tab(label='CO2 Emissions', children=emissionCO2_layout(all_data_melted)),
        # dcc.Tab(label='Search', children=search_layout(all_data_melted))
    ]),
    html.Div(id='tab-content', children='Loading...'),

])
register_tab_content_callbacks(app)
# register_overview_callbacks(app, all_data_melted)
# register_supply_callbacks(app, all_data_melted)
# register_power_callbacks(app, all_data_melted)
# register_sector_callbacks(app, all_data_melted)
# register_emissionCO2_callback(app, all_data_melted)
# register_search_callbacks(app, all_data_melted)
# register_subsector_overview_callback(app, all_data_melted)
# register_subsector_transport_callback(app, all_data_melted) 
# register_subsector_residential_callback(app,all_data_melted)
# register_subsector_services_callback(app,all_data_melted)
# register_subsector_industry_callback(app,all_data_melted)

register_overview_callbacks(app) #, all_data_melted)
register_supply_callbacks(app)#, all_data_melted)
register_power_callbacks(app)#, all_data_melted)
register_sector_callbacks(app)#, all_data_melted)
register_emissionCO2_callback(app)#, all_data_melted)
register_search_callbacks(app)#, all_data_melted)
register_subsector_overview_callback(app)#, all_data_melted)
register_subsector_transport_callback(app)#, all_data_melted) 
register_subsector_residential_callback(app)#,all_data_melted)
register_subsector_services_callback(app)#,all_data_melted)
register_subsector_industry_callback(app)#,all_data_melted)



if __name__ == '__main__':
    app.run(debug=True)

