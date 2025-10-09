
# CO2-emissions-chart
from dash import Input, Output
from utils.plot_chart import plot_chart
from utils.dataframe_melter import get_data_melted
def register_emissionCO2_callback(app):#, all_data_melted):
    all_data_melted = get_data_melted()
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