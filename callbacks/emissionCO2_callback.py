
# CO2-emissions-chart
from dash import Input, Output
import plotly.express as px
from utils.table_series_name import get_series_name
from utils.plot_chart import plot_chart

def register_emissionCO2_callback(app, all_data_melted):
    @app.callback(
        Output('CO2-emissions-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('CO2-emissions-radio', 'value')
    )
    def CO2_emissions(scenario, year_range, CO2_emissions_radio):
        
        table_name = CO2_emissions_radio

        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == table_name)]
        
        return plot_chart(all_data_melted_filtered)