from dash import html, dcc

subsector_services = html.Div([
                        html.H3("Services Sector"),
                        html.Div([
                            html.Label("TFC"),
                            dcc.Dropdown(
                                id = 'services-tfc-dropdown',
                                options=['comercial space/water heating', 'public space water heating', 'by service'],
                                value='by service'
                            ),dcc.Graph(id ='services-tfc-chart')
                        ]),
                        html.Div([
                            html.Label('Data center'),
                            dcc.Dropdown(
                                id= 'service-datacenter-dropdown',
                                options= ['electricity demand', 'excess heat potential', 'dc exccess heat supply to DH grid'],
                                value= 'electricity demand'
                            ),dcc.Graph(id='service-datacenter-chart')
                        ])
                    ])