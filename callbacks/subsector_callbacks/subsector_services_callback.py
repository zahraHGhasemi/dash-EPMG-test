
from dash import Input, Output
from utils.plot_chart import plot_chart
from utils.dataframe_melter import get_data_melted

def register_subsector_services_callback(app):#,all_data_melted):
    all_data_melted = get_data_melted()
    @app.callback(
        Output('services-tfc-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('services-tfc-dropdown', 'value')
    )
    def FEC_by_service_tfc(scenario, year_range, service):
        if service == 'comercial space/water heating':
            service_f = 'SRV-COM_FEC_WS'
        elif service == 'public space water heating':
            service_f = 'SRV-PUB_FEC_WS'
        elif service == 'by service':
            service_f = 'SRV_FEC_Service'
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == service_f)]
        return plot_chart(all_data_melted_filtered)

    @app.callback(
        Output('service-datacenter-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('service-datacenter-dropdown', 'value')
    )

    def service_datacenter(scenario, year_range, service):
        if service == 'electricity demand':
            service_f = 'SRV_FEC_DCs'
        elif service == 'excess heat potential':
            service_f = 'SRV-DCs_EH'
        elif service == 'dc exccess heat supply to DH grid':
            service_f = 'SRV-DCs_EH_DH-Grid'
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == service_f)]

        return plot_chart(all_data_melted_filtered)