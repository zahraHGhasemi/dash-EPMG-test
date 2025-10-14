from dash import Input, Output, State
from utils.filter_dataframe import filter_df_by_category    
from dash import dcc, html
from utils.plot_chart import plot_chart
from utils.dataframe_melter import get_data_melted
def register_search_callbacks(app):#, all_data_melted):
    
    @app.callback(
        Output("search-results-container", "children"),
        Input("apply-filter-btn", "n_clicks"),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('chart-type-dropdown', 'value'),
        State("include-words-input", "value"),
        State("exclude-words-input", "value")
    )
    def search_callback(n_clicks, scenario, year_range, chart_type, include_words, exclude_words):
        all_data_melted = get_data_melted(scenario, year_range)

        if not n_clicks:
            return [html.P("Enter filters and click Apply to see results.")]

        include_list = [w.strip() for w in include_words.split(',')] if include_words else []
        exclude_list = [w.strip() for w in exclude_words.split(',')] if exclude_words else []
        
        df_filtered = filter_df_by_category(
            df=all_data_melted,
            existing_words=include_list,
            non_existing_words=exclude_list
        )

        if df_filtered.empty:
            return [html.P("No results found with selected filters.")]

        figures = []
        unique_tables = df_filtered['tableName'].unique()
        figures = []
        for table in unique_tables:
            df_table = df_filtered[df_filtered['tableName'] == table]
            fig = plot_chart(df_table, type= chart_type)

            figures.append(
                html.Div([
                    html.H4(df_table['tableTitle'].iloc[0]),
                    dcc.Graph(figure=fig)
                ], style={"marginBottom": "40px"})
            )

        return figures