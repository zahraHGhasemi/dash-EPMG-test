from dash import dcc
from dash import html

power_layout = html.Div([
                dcc.Dropdown(
                id='capacity-dropdown',
                options=['Installed Capacity','New Capacity'],
                value='New Capacity',
                placeholder="Select the capacity...",
                multi = False
                ),
                dcc.Graph(id='capacity-chart'),
                dcc.Graph(id='CO2-emission-power'),
                dcc.Graph(id='Electricity-generation-PP')
            ])

        