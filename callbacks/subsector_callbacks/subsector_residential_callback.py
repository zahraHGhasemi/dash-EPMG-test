from dash import Input, Output
from utils.plot_chart import plot_chart
from utils.dataframe_melter import get_data_melted

def register_subsector_residential_callback(app):#,all_data_melted):
    
    @app.callback(
        Output('residential-house-stock-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('residential-house-stock-dropdown', 'value')
    )
    def residential_house_stock(scenario, year_range, house_stock):
        all_data_melted = get_data_melted(scenario, year_range)
        if house_stock == 'Number of Dwellings by Type':
            house_stock_f = 'RSD_BLD_TYPE'
        elif house_stock == 'New Dwellings by Type':
            house_stock_f = 'RSD_BLD-N_TYPE'
        all_data_melted_filtered = all_data_melted[(all_data_melted['tableName'] == house_stock_f)]
        return plot_chart(all_data_melted_filtered)

    @app.callback(
        Output('residential-retrofit-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('residential-retrofit-dropdown', 'value')
    )
    def residential_retrofit(scenario, year_range, retrofit):
        all_data_melted = get_data_melted(scenario, year_range)

        if retrofit == 'apartment':
            retrofit_f = 'RSD_RTFT-APT_NCAP'
        elif retrofit == 'attached':
            retrofit_f = 'RSD_RTFT-ATT_NCAP'
        elif retrofit == 'detached':
            retrofit_f = 'RSD_RTFT-DET_NCAP'
        elif retrofit == 'energy saving':
            retrofit_f = 'RSD_RTFT_NRG_SAVINGS'
        all_data_melted_filtered = all_data_melted[all_data_melted['tableName'] == retrofit_f]
        # print(all_data_melted_filtered['seriesTitle'].unique())
        # print(all_data_melted_filtered['seriesName'].unique())
        return plot_chart(all_data_melted_filtered, 'bar')


    @app.callback(
        Output('residential-FEC-by-service-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value')
    )
    def residential_FEC_by_service(scenario, year_range):
        all_data_melted = get_data_melted(scenario, year_range)

        all_data_melted_filtered = all_data_melted[(all_data_melted['tableName'] == "RSD_Services_EnergyCons")]
        return plot_chart(all_data_melted_filtered)


    @app.callback(
        Output('residential-FEC-bysector-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('residential-FEC-bysector-dropdown', 'value')
    )
    def residential_FEC_bysector(scenario, year_range, selected_sector):
        all_data_melted = get_data_melted(scenario, year_range)

        if selected_sector == "Water and Space Heating":
            sector = "RSD_WaterSpace_FuelCons"
        elif selected_sector == "Space/Water in Apartments":
            sector = "RSD_WS-APT_FuelCons"
        elif selected_sector == "Space/Water in Attached":
            sector = "RSD_WS-ATT_FuelCons"
        elif selected_sector == "Space/Water in Detached":
            sector = "RSD_WS-DET_FuelCons"
        elif selected_sector == "Other Services":
            sector = "RSD_OtherServices_FuelCons"

        all_data_melted_filtered = all_data_melted[(all_data_melted['tableName'] == sector)]
        return plot_chart(all_data_melted_filtered)
