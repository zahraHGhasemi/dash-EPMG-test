from dash import Input, Output
from utils.plot_chart import plot_chart
from utils.filter_dataframe import filter_df_by_category
from utils.dataframe_melter import get_data_melted

def register_subsector_transport_callback(app):#, all_data_melted):
    all_data_melted = get_data_melted()
    df_filtered_FC = filter_df_by_category(all_data_melted, ['TRA','Fuel'])
    df_filtered_VS = filter_df_by_category(all_data_melted, ['TRA', 'TYPE'],['Fuel'])
    df_filtered_VA = filter_df_by_category(all_data_melted, ['TRA', 'Land'])
    dic_filter_FC = dict(zip(df_filtered_FC['tableTitle'].unique(),df_filtered_FC['tableName'].unique()))
    dic_filter_VS = dict(zip(df_filtered_VS['tableTitle'].unique(),df_filtered_VS['tableName'].unique()))
    dic_filter_VA = dict(zip(df_filtered_VA['tableTitle'].unique(),df_filtered_VA['tableName'].unique()))

    @app.callback(
        Output('transport-fuel-cons-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('transport-fuel-cons-dropdown', 'value')
    )

    def transport_fuel_cons(scenario, year_range, fuel_cons):
        # dic_filter = {'Fuel Consumption - Domestic Aviation': 'TRA_AVIDOM_FuelCons',
        #             'Fuel Consumption - International Aviation': 'TRA_AVIINT_FuelCons',
        #             'Fuel Consumption - Land Transport (F)': 'TRA_Freight_Land_FuelCons',
        #             'Fuel Consumption - Navigation': 'TRA_NAV_FuelCons',
        #             'Fuel Consumption - Unspecified': 'TRA_OTH_FuelCons',
        #             'Fuel Consumption - Land Transport (P)': 'TRA_Passenger_Land_FuelCons',
        #             'Fuel Consumption - Tourism': 'TRA_TURS_FuelCons'}
        dic_filter = dic_filter_FC
        table_name = dic_filter[fuel_cons]

        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'] == table_name)]
        
        return plot_chart(all_data_melted_filtered)
    
    
    @app.callback(
        Output('transport-vehicle-type-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('transport-vehicle-type-dropdown', 'value')
    )
    def transport_vehicle_type(scenario, year_range, vehicle_type):
        # transport_fc = filter_df_by_category(all_data_melted, ['TRA',"TYPE"])
        # dic_filter = dict(zip(transport_fc['tableTitle'].unique(),transport_fc['tableName'].unique()))

        # dic_filter = {'New HGV - Stock by Type': 'TRA_F-HTRUCK-N_TYPE',
        #             'HGV - Stock by Type': 'TRA_F-HTRUCK_TYPE',
        #             'New LGV - Stock by Type': 'TRA_F-LTRUCK-N_TYPE',
        #             'LGV - Stock by Type': 'TRA_F-LTRUCK_TYPE',
        #             'New MGV - Stock by Type': 'TRA_F-MTRUCK-N_TYPE',
        #             'MGV - Stock by Type': 'TRA_F-MTRUCK_TYPE',
        #             'New Private Cars - Stock by Type': 'TRA_P-CAR-N_TYPE',
        #             'Private Cars - Stock by Type': 'TRA_P-CAR_TYPE'}
        dic_filter = dic_filter_VS
        table_name = dic_filter[vehicle_type]
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName']== table_name)]
        return plot_chart(all_data_melted_filtered)


    @app.callback(
        Output('transport-vehicle-activity-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('transport-vehicle-activity-dropdown', 'value')
    )
    def transport_vehicle_activity(scenario, year_range, vehicle_activity):
        # dic_filtered = {'Land Transport - Lump Sum Investment Cost': 'TRA-Land_LumpInv',
        #                 'Land Transport (F) by Mode': 'TRA_Freight_Land_Mode',
        #                 'Land Transport (P) by Distance': 'TRA_Passenger_Land_Distance',
        #                 'Land Transport (P) by Mode': 'TRA_Passenger_Land_Mode',
        #                 'Land Transport (P) - Long': 'TRA_Passenger_Land_Mode-L',
        #                 'Land Transport (P) - Medium': 'TRA_Passenger_Land_Mode-M',
        #                 'Land Transport (P) - Short': 'TRA_Passenger_Land_Mode-S'}
        dic_filtered = dic_filter_VA
        table_name = dic_filtered[vehicle_activity]
        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName']== table_name)]
        return plot_chart(all_data_melted_filtered)
    
    @app.callback(
        Output('transport-other-chart', 'figure'),
        Input('scenario-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('transport-other-dropdown', 'value')
    )
    def transport_other(scenario, year_range, other):
        selected_table_name =[]
        if "CO2 emission" in other:
            selected_table_name.append("TRA_Emissions-CO2")
        elif "Land TransportLump Sum Investment Cost" in other:
            selected_table_name.append("TRA-Land_LumpInv")

        all_data_melted_filtered = all_data_melted[(all_data_melted['Scenario'] == scenario) &
                                                    (all_data_melted['Year'] >= year_range[0]) &
                                                    (all_data_melted['Year'] <= year_range[1])&
                                                    (all_data_melted['tableName'].isin(selected_table_name))]
        return plot_chart(all_data_melted_filtered)
