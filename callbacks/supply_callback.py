
from dash import Input, Output
from utils.table_series_name import get_table_id 
from utils.plot_chart import plot_chart
from utils.dataframe_melter import get_data_melted
def register_supply_callbacks(app):#, all_data_melted):
    all_data_melted = get_data_melted()
    @app.callback(
        Output('supply-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('supply-source-dropdown', 'value')
    )
    def supply_chart(scenario, year_range, supply_source):
        table_name = get_table_id(supply_source)
        

        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
            (all_data_melted['Year'] >= year_range[0]) &
            (all_data_melted['Year'] <= year_range[1])&
            (all_data_melted['tableName']== table_name)]
        return plot_chart(all_data_melted_filtered)
        

    @app.callback(
        Output('Hydrogen Production', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value')
    )
    def hydrogen_production(scenario, year_range):
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                (all_data_melted['Year'] >= year_range[0]) &
                (all_data_melted['Year'] <= year_range[1])&
                (all_data_melted['tableName']== "SUP_HYDROGEN")]
        return plot_chart(all_data_melted_filtered)
        