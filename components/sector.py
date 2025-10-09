from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

sector_layout = dbc.Row([
                    dbc.Col(
                        dcc.RadioItems(
                            id="sector-radio",
                            options=[
                                {"label": "Overview", "value": "overview"},
                                {"label": "Transport", "value": "transport"},
                                {"label": "Residential", "value": "residential"},
                                {"label": "Services", "value": "services"},
                                {"label": "Industry", "value": "industry"},
                            ],
                            value="overview",  # Default
                            labelStyle={"display": "block"}  # Vertical layout
                        ),
                        width=2
                    ),
                    # Right side: dynamic content
                    dbc.Col(html.Div(id="sector-content"), width=10)
                ])