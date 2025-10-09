from dash import dcc, html

def search_layout(df):
    return (
        html.Div([
            html.H3("Search and Filter Plots"),

            html.Div([
                html.Label("Include words (comma-separated):"),
                dcc.Input(
                    id="include-words-input",
                    type="text",
                    placeholder="e.g. SYS, Sector, FEC",
                    style={"width": "80%", "margin-bottom": "10px"}
                ),
                html.Label("Exclude words (comma-separated):"),
                dcc.Input(
                    id="exclude-words-input",
                    type="text",
                    placeholder="e.g. Cost, Lump",
                    style={"width": "80%", "margin-bottom": "10px"}
                ),
                html.Button("Apply Filter", id="apply-filter-btn", n_clicks=0)
            ], style={"margin-bottom": "20px"}),

            # Container for dynamically generated graphs
            html.Div(id="search-results-container")
        ])

    )