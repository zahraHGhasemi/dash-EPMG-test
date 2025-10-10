from dash import Input, Output
import plotly.express as px
from utils.dataframe_melter import get_data_melted

def register_overview_callbacks(app):#, all_data_melted):
    @app.callback(
        Output('import-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-input', 'value')
    )
    def update_import_chart(scenario, year):
        all_data_melted = get_data_melted(scenario, [year, year])

        filtered_df = all_data_melted[(all_data_melted['tableName'] == 'SYS_NRG-Import')]
        fig = px.pie(filtered_df, values='Value', names='seriesTitle', title=f'Import ({year})')
        return fig

    @app.callback(
        Output('export-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-input', 'value')
    )
    def update_export_chart(scenario, year):
        all_data_melted = get_data_melted(scenario, [year, year])

        filtered_df = all_data_melted[(all_data_melted['tableName'] == 'SYS_FEC_Fuel')]
        fig = px.pie(filtered_df, values='Value', names='seriesTitle', title=f'FEC ({year})')
        return fig
