from dash import html, dcc

subsector_industry = html.Div([
                        html.H3("Industry Sector"),
                        html.Div([
                            html.Label("Subsector:"),
                            dcc.Dropdown(
                                id= 'industry-subsector-dropdown',
                                options=['wood and wood product','other non-metalix mineral products', 'cement', 'other manufactuting', 'lime', 'chemical and man-made fibre', 'food and beverages',
                                        'basic metal and fabricated metal products'],
                                value= 'wood and wood product',
                                multi = False
                            ),dcc.Graph(id = 'industry-subsector-chart')
                        ])
                    ])
