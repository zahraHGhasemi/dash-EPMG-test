from dash import dcc
from dash import html


supply_layout=html.Div([
                html.Label("Select suuply by source:"),
                dcc.Dropdown(
                    id = 'supply-source-dropdown',
                    options = ['Biodiesel Supply by Source',
                                'Ethanol Supply by Source',
                                'Biogas Supply by Source'],
                    value = 'Biodiesel Supply by Source',
                    multi = False
                ),
                dcc.Graph(id = 'supply-chart'),
                dcc.Graph(id = "Hydrogen Production")
            ])

        