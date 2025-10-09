from dash import Input, Output
from utils.plot_chart import plot_chart

def register_subsector_industry_callback(app,all_data_melted):
        
    @app.callback(
        Output('industry-subsector-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('industry-subsector-dropdown', 'value')
    )
    def industry_subsector(scenario, year_range, subsector):
        ls_subsector=[]
        if 'wood and wood product' in subsector:
            ls_subsector.append('IND-WAP_FEC'),
        if 'other non-metalix mineral products' in subsector:
            ls_subsector.append('IND-ONM_FEC')
        if 'cement' in subsector:
            ls_subsector.append('IND-CEM_FEC')
        if 'other manufactuting' in subsector:
            ls_subsector.append('IND-OMA_FEC')
        if 'lime' in subsector:
            ls_subsector.append('IND-LIM_FEC')
        if 'chemical and man-made fibre' in subsector:
            ls_subsector.append('IND-CAF_FEC')
        if 'food and beverages' in subsector:
            ls_subsector.append('IND-FAP_FEC')
        if 'basic metal and fabricated metal products' in subsector:
            ls_subsector.append('IND-MAP_FEC')

        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'].isin(ls_subsector))]
        return plot_chart(all_data_melted_filtered)

