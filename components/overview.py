import dash_bootstrap_components as dbc
from dash import html, dcc
overview_layout = dbc.Container([
    html.H2("Overview", className="mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([   
                  html.H4("Emissions", className="card-title"),
                  html.P(
                      "Energy-related CO2 emissions, Ireland, 2022", className="card-text"
                  ),
                  html.H5("Ireland, 2022", className="card-subtitle"),
                  html.H3("33 Mt CO₂", className="card-text"),
                  html.H5("0.1% of global emissions", className="card-text")
                ])
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([   
                  html.H4("Renewables", className="card-title"),

                  html.H3("38.9%", className="card-text"),
                  html.H5("share of power generation, 2022", className="card-text"),
                ])
            ),
            width=3
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([   
                  html.H4("Electricity consumption per capita", className="card-title"),

                  html.H3("↑9%", className="card-text"),
                  html.H5("change 2000-2024", className="card-text"),
                ])
            ),
            width=3
        ),
    ], className="mb-4"),
    dcc.Input(
        id="year-input",
        type="number",
        min=2018,
        max = 2050,
        placeholder="e.g. 2024",
        value = 2024,
        style={"width": "50%", "margin-bottom": "10px"}
    ),
    dbc.Row([
        dbc.Col(
        [
            html.Button(
                "↓",
                id='import-export-download',
                
            ),
            dcc.Graph(id='import-chart',
                      style={'height': '400px'},
                    config={'responsive': True})
            
        ],
            md=6,  # 6/12 width = half of the row on medium+ screens
        ),
        dbc.Col(
        [
            html.Button(
                "↓",
                id='import-export-download',
                
            ),
            dcc.Graph(id='export-chart',
                      style={'height': '400px'},
                    config={'responsive': True})
            
        ],
            md=6
        ),
    ])
    
    
    # You can add more rows with graphs/tables here
])