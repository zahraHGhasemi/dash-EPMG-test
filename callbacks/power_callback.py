
# capacity-chart
# co2-emission-power
# electricity-generation-PP
from dash import Input, Output
from utils.table_series_name import get_table_id
from utils.plot_chart import plot_chart
from utils.dataframe_melter import get_data_melted
def register_power_callbacks(app):#, all_data_melted):
    all_data_melted = get_data_melted()
    @app.callback(
        Output('capacity-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('capacity-dropdown', 'value')
    )
    def capacity_chart(scenario, year_range, capacity_type):
        table_name = get_table_id(capacity_type)
       
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == table_name)]
        
        return plot_chart(all_data_melted_filtered)
    @app.callback(
        Output('CO2-emission-power', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
    )
    def co2_emission_power(scenario, year_range):
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == "PWR_Emissions-CO2")]

        return plot_chart(all_data_melted_filtered)
    @app.callback(
        Output('Electricity-generation-PP', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
    )
    def elec_generation(scenario, year_range):
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == "PWR_Gen-ELCC")]

        return plot_chart(all_data_melted_filtered)
