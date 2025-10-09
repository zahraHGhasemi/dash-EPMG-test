from dash import html, dcc
subsector_residential = html.Div([
                            html.H3("Residential Sector"),
                            html.Div([
                                html.Label("FEC by subsector:"),
                                dcc.Dropdown(
                                    id = "residential-FEC-bysector-dropdown",
                                    options=['Water and Space Heating', 'Space/Water in Apartments', 'Space/Water in Attached', 'Space/Water in Detached',  'Other Services'],
                                    value = 'Water and Space Heating',
                                    multi = False
                                ),dcc.Graph(id ="residential-FEC-bysector-chart")
                            ]),
                            html.Div([
                                html.Label("FEC by service"),
                                dcc.Graph(id = 'residential-FEC-by-service-chart')
                            ]),
                            html.Div([
                                html.Label('Retrofits'),
                                dcc.Dropdown(
                                    id = 'residential-retrofit-dropdown',
                                    options= [{'label': 'apartment', 'value': 'apartment'}, {'label': 'attached', 'value': 'attached'}, {'label': 'detached', 'value': 'detached'},{'label': 'energy saving', 'value': 'energy saving'}],
                                    value = 'apartment',
                                ),dcc.Graph(id = "residential-retrofit-chart")
                            ]),
                            html.Div([
                                html.Label("House stock"),
                                dcc.Dropdown(
                                    id="residential-house-stock-dropdown",
                                    options= ['Number of Dwellings by Type', 'New Dwellings by Type'],
                                    value= 'Number of Dwellings by Type'
                                ),dcc.Graph(id= 'residential-house-stock-chart')
                            ])
                        ])
