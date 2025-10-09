import dash_bootstrap_components as dbc
from dash import html
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
                  html.H5("0.1% of global emissions", className="card-text"),
                  dbc.Button("Emission", color="primary", id = "emission-button"),

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

    # You can add more rows with graphs/tables here
])